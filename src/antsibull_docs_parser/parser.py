# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""
Parser for formatted texts.
"""

from __future__ import annotations

import abc
import re
import typing as t
from enum import Enum as _Enum

from . import dom
from ._parser_impl import parse_parameters_escaped, parse_parameters_unescaped

_IGNORE_MARKER = "ignore:"
_ARRAY_STUB_RE = re.compile(r"\[([^\]]*)\]")
_FQCN_TYPE_PREFIX_RE = re.compile(r"^([^.]+\.[^.]+\.[^#]+)#([^:]+):(.*)$")
_FQCN = re.compile(r"^[A-Za-z0-9_]+\.[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)+$")
_PLUGIN_TYPE = re.compile(r"^[a-z_]+$")
_WHITESPACE = re.compile(r"([\s]+)")
_DANGEROUS_WS = re.compile(r"[\t\n\r]")
_SPACES_TO_KEEP = re.compile(
    "([\u00a0\u202f\u2007\u2060\u200b\u200c\u200d\ufeff]+)", flags=re.UNICODE
)


def _is_fqcn(text: str) -> bool:
    return _FQCN.match(text) is not None


def _is_plugin_type(text: str) -> bool:
    # We do not want to hard-code a list of valid plugin types that might be
    # inaccurate, so we simply check whether this is a valid kind of Python
    # identifier usually used for plugin types. If ansible-core ever adds one
    # with digits, we'll have to update this.
    return _PLUGIN_TYPE.match(text) is not None


def _repr(text: str) -> str:
    # Do something like repr(), but prefer double quotes
    text = repr(text)
    return f'"{text[1:-1]}"'


class Whitespace(_Enum):
    # Keep all whitespace as-is.
    IGNORE = 0

    # Reduce all whitespace (space, tabs, newlines, ...) to regular breakable or
    # non-breakable spaces. Multiple spaces are kept in everything that's often
    # rendered code-style, like C(), O(), V(), RV(), E().
    STRIP = 1

    # Similar to STRIP, but keep single newlines intact.
    KEEP_SINGLE_NEWLINES = 2


def _add_whitespace(
    result: list[str],
    ws: str,
    *,
    whitespace: Whitespace,
    no_newlines: bool = False,
) -> None:
    if (
        whitespace == Whitespace.KEEP_SINGLE_NEWLINES
        and not no_newlines
        and any(lb in ws for lb in "\n\r")
    ):
        result.append("\n")
    else:
        result.append(" ")


def _process_whitespace(
    text: str,
    *,
    whitespace: Whitespace,
    code_environment: bool = False,
    no_newlines: bool = False,
) -> str:
    if whitespace == Whitespace.IGNORE:
        return text
    length = len(text)
    index = 0
    result = []
    while index < length:
        m = _WHITESPACE.search(text, index)
        if m is None:
            result.append(text[index:])
            break
        if m.start(1) > index:
            result.append(text[index : m.start(1)])
        ws = m.group(1)
        if code_environment:
            result.append(_DANGEROUS_WS.sub(" ", ws))
        else:
            ws_index = 0
            ws_length = len(ws)
            while ws_index < ws_length:
                wsm = _SPACES_TO_KEEP.search(ws, ws_index)
                if wsm is None:
                    _add_whitespace(
                        result,
                        ws[ws_index:],
                        whitespace=whitespace,
                        no_newlines=no_newlines,
                    )
                    break
                if wsm.start(1) > ws_index:
                    _add_whitespace(
                        result,
                        ws[ws_index : wsm.start(1)],
                        whitespace=whitespace,
                        no_newlines=no_newlines,
                    )
                result.append(wsm.group(1))
                ws_index = wsm.end(1)
        index = m.end(1)
    return "".join(result)


class Context(t.NamedTuple):
    current_plugin: dom.PluginIdentifier | None = None
    role_entrypoint: str | None = None


class CommandParser(abc.ABC):
    command: str
    parameters: int
    escaped_arguments: bool
    strip_surrounding_whitespace: bool

    def __init__(
        self,
        command: str,
        parameters: int,
        escaped_arguments: bool = False,
        *,
        strip_surrounding_whitespace: bool = False,
    ):
        self.command = command
        self.parameters = parameters
        self.escaped_arguments = escaped_arguments
        self.strip_surrounding_whitespace = strip_surrounding_whitespace

    @abc.abstractmethod
    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        pass  # pragma: no cover


class CommandParserEx(CommandParser):
    old_markup: bool

    def __init__(
        self,
        command: str,
        parameters: int,
        escaped_arguments: bool = False,
        old_markup: bool = False,
        *,
        strip_surrounding_whitespace: bool = False,
    ):
        super().__init__(
            command,
            parameters,
            escaped_arguments=escaped_arguments,
            strip_surrounding_whitespace=strip_surrounding_whitespace,
        )
        self.old_markup = old_markup


# Classic Ansible docs markup:


class _Italics(CommandParserEx):
    def __init__(self):
        super().__init__("I", 1, old_markup=True)

    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        return dom.ItalicPart(
            text=_process_whitespace(
                parameters[0], whitespace=whitespace, no_newlines=True
            ),
            source=source,
        )


class _Bold(CommandParserEx):
    def __init__(self):
        super().__init__("B", 1, old_markup=True)

    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        return dom.BoldPart(
            text=_process_whitespace(
                parameters[0], whitespace=whitespace, no_newlines=True
            ),
            source=source,
        )


class _Module(CommandParserEx):
    def __init__(self):
        super().__init__("M", 1, old_markup=True)

    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        fqcn = _process_whitespace(
            parameters[0], whitespace=whitespace, no_newlines=True
        )
        if not _is_fqcn(fqcn):
            raise ValueError(f"Module name {_repr(fqcn)} is not a FQCN")
        return dom.ModulePart(fqcn=fqcn, source=source)


class _URL(CommandParserEx):
    def __init__(self):
        super().__init__("U", 1, old_markup=True)

    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        return dom.URLPart(
            url=_process_whitespace(
                parameters[0], whitespace=whitespace, no_newlines=True
            ),
            source=source,
        )


class _Link(CommandParserEx):
    def __init__(self):
        super().__init__("L", 2, old_markup=True)

    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        text = _process_whitespace(
            parameters[0], whitespace=whitespace, no_newlines=True
        )
        url = _process_whitespace(
            parameters[1], whitespace=whitespace, no_newlines=True
        )
        return dom.LinkPart(text=text, url=url, source=source)


class _RSTRef(CommandParserEx):
    def __init__(self):
        super().__init__("R", 2, old_markup=True)

    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        text = _process_whitespace(
            parameters[0], whitespace=whitespace, no_newlines=True
        )
        ref = _process_whitespace(
            parameters[1], whitespace=whitespace, no_newlines=True
        )
        return dom.RSTRefPart(text=text, ref=ref, source=source)


class _Code(CommandParserEx):
    def __init__(self):
        super().__init__("C", 1, old_markup=True)

    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        return dom.CodePart(
            text=_process_whitespace(
                parameters[0],
                whitespace=whitespace,
                code_environment=True,
                no_newlines=True,
            ),
            source=source,
        )


class _HorizontalLine(CommandParserEx):
    def __init__(self):
        super().__init__(
            "HORIZONTALLINE", 0, old_markup=True, strip_surrounding_whitespace=True
        )

    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        return dom.HorizontalLinePart(source=source)


# Semantic Ansible docs markup:


def _parse_option_like(
    text: str,
    context: Context,
) -> tuple[
    dom.PluginIdentifier | None,
    str | None,
    list[str],
    str,
    str | None,
]:
    value = None
    if "=" in text:
        text, value = text.split("=", 1)
    entrypoint: str | None = None
    m = _FQCN_TYPE_PREFIX_RE.match(text)
    if m:
        plugin_fqcn = m.group(1)
        plugin_type = m.group(2)
        if not _is_fqcn(plugin_fqcn):
            raise ValueError(f"Plugin name {_repr(plugin_fqcn)} is not a FQCN")
        if not _is_plugin_type(plugin_type):
            raise ValueError(f"Plugin type {_repr(plugin_type)} is not valid")
        plugin_identifier = dom.PluginIdentifier(fqcn=plugin_fqcn, type=plugin_type)
        text = m.group(3)
    elif text.startswith(_IGNORE_MARKER):
        plugin_identifier = None
        text = text[len(_IGNORE_MARKER) :]
    else:
        plugin_identifier = context.current_plugin
        entrypoint = context.role_entrypoint
    if plugin_identifier is not None and plugin_identifier.type == "role":
        part1, sep, part2 = text.partition(":")
        if sep:
            entrypoint = part1
            text = part2
        if entrypoint is None:
            raise ValueError("Role reference is missing entrypoint")
    if ":" in text or "#" in text:
        raise ValueError(f"Invalid option/return value name {_repr(text)}")
    return (
        plugin_identifier,
        entrypoint,
        _ARRAY_STUB_RE.sub("", text).split("."),
        text,
        value,
    )


class _Plugin(CommandParserEx):
    def __init__(self):
        super().__init__("P", 1, escaped_arguments=True)

    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        name = _process_whitespace(
            parameters[0], whitespace=whitespace, no_newlines=True
        )
        if "#" not in name:
            raise ValueError(f"Parameter {_repr(name)} is not of the form FQCN#type")
        fqcn, ptype = name.split("#", 1)
        if not _is_fqcn(fqcn):
            raise ValueError(f"Plugin name {_repr(fqcn)} is not a FQCN")
        if not _is_plugin_type(ptype):
            raise ValueError(f"Plugin type {_repr(ptype)} is not valid")
        return dom.PluginPart(
            plugin=dom.PluginIdentifier(fqcn=fqcn, type=ptype), source=source
        )


class _EnvVar(CommandParserEx):
    def __init__(self):
        super().__init__("E", 1, escaped_arguments=True)

    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        return dom.EnvVariablePart(
            name=_process_whitespace(
                parameters[0],
                whitespace=whitespace,
                code_environment=True,
                no_newlines=True,
            ),
            source=source,
        )


class _OptionValue(CommandParserEx):
    def __init__(self):
        super().__init__("V", 1, escaped_arguments=True)

    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        return dom.OptionValuePart(
            value=_process_whitespace(
                parameters[0],
                whitespace=whitespace,
                code_environment=True,
                no_newlines=True,
            ),
            source=source,
        )


class _OptionName(CommandParserEx):
    def __init__(self):
        super().__init__("O", 1, escaped_arguments=True)

    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        plugin, entrypoint, link, name, value = _parse_option_like(
            _process_whitespace(
                parameters[0],
                whitespace=whitespace,
                code_environment=True,
                no_newlines=True,
            ),
            context,
        )
        return dom.OptionNamePart(
            plugin=plugin,
            entrypoint=entrypoint,
            link=link,
            name=name,
            value=value,
            source=source,
        )


class _ReturnValue(CommandParserEx):
    def __init__(self):
        super().__init__("RV", 1, escaped_arguments=True)

    def parse(
        self,
        parameters: list[str],
        context: Context,
        source: str | None,
        whitespace: Whitespace,
    ) -> dom.AnyPart:
        plugin, entrypoint, link, name, value = _parse_option_like(
            _process_whitespace(
                parameters[0],
                whitespace=whitespace,
                code_environment=True,
                no_newlines=True,
            ),
            context,
        )
        return dom.ReturnValuePart(
            plugin=plugin,
            entrypoint=entrypoint,
            link=link,
            name=name,
            value=value,
            source=source,
        )


_COMMANDS = [
    _Italics(),
    _Bold(),
    _Module(),
    _URL(),
    _Link(),
    _RSTRef(),
    _Code(),
    _HorizontalLine(),
    _Plugin(),
    _EnvVar(),
    _OptionValue(),
    _OptionName(),
    _ReturnValue(),
]


def _command_re(command: CommandParser) -> str:
    return (
        r"\b"
        + re.escape(command.command)
        + (r"\b" if command.parameters == 0 else r"\(")
    )


class Parser:
    _group_map: t.Mapping[str, CommandParser]
    _re: re.Pattern

    def __init__(self, commands: t.Sequence[CommandParser]):
        self._group_map = {
            cmd.command + ("(" if cmd.parameters else ""): cmd for cmd in commands
        }
        if commands:
            self._re = re.compile(
                "(" + "|".join([_command_re(cmd) for cmd in commands]) + ")"
            )
        else:
            self._re = re.compile("x^")  # does not match anything

    @staticmethod
    def _parse_command(
        result: dom.Paragraph,
        text: str,
        cmd: CommandParser,
        index: int,
        end_index: int,
        context: Context,
        errors: dom.ErrorType,
        where: str,
        *,
        strict: bool,
        add_source: bool,
        helpful_errors: bool,
        whitespace: Whitespace,
        offset: int,
    ) -> int:
        args: list[str]
        error: str | None = None
        if cmd.parameters == 0:
            args = []
        elif cmd.escaped_arguments:
            args, end_index, error = parse_parameters_escaped(
                text, end_index, cmd.parameters, strict=strict
            )
        else:
            args, end_index, error = parse_parameters_unescaped(
                text, end_index, cmd.parameters, strict=strict
            )
        source = text[index:end_index] if add_source else None
        if error is None:
            try:
                result.append(
                    cmd.parse(args, context, source=source, whitespace=whitespace)
                )
            except Exception as exc:  # pylint:disable=broad-except
                error = f"{exc}"
        if error is not None:
            error_source = (
                _repr(text[index:end_index])
                if helpful_errors
                else f'{cmd.command}{"()" if cmd.parameters else ""}'
            )
            error = f"While parsing {error_source} at index {index + offset}{where}: {error}"
            if errors == "message":
                result.append(dom.ErrorPart(message=error, source=source))
            elif errors == "exception":
                raise ValueError(error)
        return end_index

    @staticmethod
    def _create_text(
        text: str, add_source: bool, whitespace: Whitespace
    ) -> dom.TextPart:
        text_ws = _process_whitespace(text, whitespace=whitespace)
        return dom.TextPart(text=text_ws, source=text if add_source else None)

    def parse_string(
        self,
        text: str,
        context: Context,
        errors: dom.ErrorType = "message",
        where: str = "",
        strict: bool = False,
        add_source: bool = False,
        helpful_errors: bool = True,
        *,
        whitespace: Whitespace = Whitespace.IGNORE,
    ) -> dom.Paragraph:
        offset = 1
        if whitespace != Whitespace.IGNORE:
            old_length = len(text)
            text = text.lstrip()
            offset += old_length - len(text)
            text = text.rstrip()

        result: dom.Paragraph = []
        length = len(text)
        index = 0
        while index < length:
            m = self._re.search(text, index)
            if m is None:
                result.append(self._create_text(text[index:], add_source, whitespace))
                break
            cmd = self._group_map[m.group(1)]
            if m.start(1) > index:
                pretext = text[index : m.start(1)]
                if cmd.strip_surrounding_whitespace:
                    pretext = pretext.rstrip(" \t")
                result.append(self._create_text(pretext, add_source, whitespace))
            index = self._parse_command(
                result,
                text,
                cmd,
                m.start(1),
                m.end(1),
                context,
                errors,
                where,
                strict=strict,
                add_source=add_source,
                helpful_errors=helpful_errors,
                whitespace=whitespace,
                offset=offset,
            )
            if cmd.strip_surrounding_whitespace:
                while index < length and text[index] in " \t":
                    index += 1
        return result


_CLASSIC = Parser([cmd for cmd in _COMMANDS if cmd.old_markup])
_SEMANTIC_MARKUP = Parser(_COMMANDS)


def parse(
    text: str | t.Sequence[str],
    context: Context,
    errors: dom.ErrorType = "message",
    only_classic_markup: bool = False,
    strict: bool = False,
    add_source: bool = False,
    helpful_errors: bool = True,
    *,
    whitespace: Whitespace = Whitespace.IGNORE,
) -> list[dom.Paragraph]:
    """
    Parse a string, or a sequence of strings, to a list of paragraphs.

    :param text: A string or a sequence of strings. If given a sequence of strings, will assume
        that this is a list of paragraphs.
    :param context: Contextual information.
    :param errors: How to handle errors while parsing.
    :param only_classic_markup: Whether to ignore semantic markup and treat it as raw text.
    :param strict: Whether to be extra strict while parsing.
    :param add_source: Whether to add the source of every part to the part (``source`` property).
    :param helpful_errors: Whether to include the faulty markup in error messages.
    :param whitespace: How to handle whitespace.
    :return: A list of paragraphs. Each paragraph consists of a list of parts.
    """
    has_paragraphs = True
    if isinstance(text, str):
        has_paragraphs = False
        text = [text] if text else []
    parser = _CLASSIC if only_classic_markup else _SEMANTIC_MARKUP
    return [
        parser.parse_string(
            par,
            context,
            errors=errors,
            where=f" of paragraph {index + 1}" if has_paragraphs else "",
            strict=strict,
            add_source=add_source,
            helpful_errors=helpful_errors,
            whitespace=whitespace,
        )
        for index, par in enumerate(text)
    ]
