# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
ReStructured Text serialization.
"""

from __future__ import annotations

import re
import typing as t

from . import dom
from .format import Formatter, LinkProvider
from .format import format_paragraphs as _format_paragraphs
from .html import _url_escape

_STARTING_WHITESPACE = re.compile(r"^\s")
_ENDING_WHITESPACE = re.compile(r"\s$")


def rst_escape(
    value: str,
    escape_ending_whitespace: bool = False,
    *,
    must_not_be_empty: bool = False,
) -> str:
    """Escape RST specific constructs."""
    value = value.replace("\\", "\\\\")
    value = value.replace("<", "\\<")
    value = value.replace(">", "\\>")
    value = value.replace("_", "\\_")
    value = value.replace("*", "\\*")
    value = value.replace("`", "\\`")
    value = value.replace("|", "\\|")

    # RST does not like it when the inside of `...` starts or ends with a whitespace
    # (here, all kind of whitespaces count, not just spaces...)
    if escape_ending_whitespace and _ENDING_WHITESPACE.match(value[-1:]):
        value = value + "\\ "
    if escape_ending_whitespace and _STARTING_WHITESPACE.match(value):
        value = "\\ " + value
    if not value and must_not_be_empty:
        value = "\\ "

    return value


class AntsibullRSTFormatter(Formatter):
    @staticmethod
    def _format_option_like(
        part: dom.OptionNamePart | dom.ReturnValuePart, role: str
    ) -> str:
        result: list[str] = []
        plugin = part.plugin
        if plugin:
            result.append(plugin.fqcn)
            result.append("#")
            result.append(plugin.type)
            result.append(":")
        entrypoint = part.entrypoint
        if entrypoint is not None:
            result.append(entrypoint)
            result.append(":")
        result.append(part.name)
        value = part.value
        if value is not None:
            result.append("=")
            result.append(value)
        text = rst_escape(
            "".join(result), escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :{role}:`{text}`\\ "

    def format_error(self, part: dom.ErrorPart) -> str:
        text = rst_escape(
            part.message, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :strong:`ERROR while parsing`\\ : {text}\\ "

    def format_bold(self, part: dom.BoldPart) -> str:
        text = rst_escape(
            part.text, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :strong:`{text}`\\ "

    def format_code(self, part: dom.CodePart) -> str:
        text = rst_escape(
            part.text, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :literal:`{text}`\\ "

    def format_horizontal_line(self, part: dom.HorizontalLinePart) -> str:
        return "\n\n.. raw:: html\n\n  <hr>\n\n"

    def format_italic(self, part: dom.ItalicPart) -> str:
        text = rst_escape(
            part.text, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :emphasis:`{text}`\\ "

    def format_link(self, part: dom.LinkPart) -> str:
        if not part.text:
            return ""
        if not part.url:
            return rst_escape(part.text)
        text = rst_escape(part.text, escape_ending_whitespace=True)
        return f"\\ `{text} <{_url_escape(part.url)}>`__\\ "

    def format_module(self, part: dom.ModulePart, url: str | None) -> str:
        text = rst_escape(
            part.fqcn, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :ref:`{text} <ansible_collections.{part.fqcn}_module>`\\ "

    def format_rst_ref(self, part: dom.RSTRefPart) -> str:
        text = rst_escape(
            part.text, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :ref:`{text} <{part.ref}>`\\ "

    def format_url(self, part: dom.URLPart) -> str:
        if not part.url:
            return ""
        url_text = rst_escape(part.url, escape_ending_whitespace=True)
        return f"\\ `{url_text} <{_url_escape(part.url)}>`__\\ "

    def format_text(self, part: dom.TextPart) -> str:
        return rst_escape(part.text)

    def format_env_variable(self, part: dom.EnvVariablePart) -> str:
        text = rst_escape(
            part.name, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :envvar:`{text}`\\ "

    def format_option_name(self, part: dom.OptionNamePart, url: str | None) -> str:
        return self._format_option_like(part, "ansopt")

    def format_option_value(self, part: dom.OptionValuePart) -> str:
        text = rst_escape(
            part.value, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :ansval:`{text}`\\ "

    def format_plugin(self, part: dom.PluginPart, url: str | None) -> str:
        return (
            f"\\ :ref:`{rst_escape(part.plugin.fqcn)} "
            f"<ansible_collections.{part.plugin.fqcn}_{part.plugin.type}>`\\ "
        )

    def format_return_value(self, part: dom.ReturnValuePart, url: str | None) -> str:
        return self._format_option_like(part, "ansretval")


class PlainRSTFormatter(Formatter):
    @staticmethod
    def _format_option_like(
        part: dom.OptionNamePart | dom.ReturnValuePart,
    ) -> str:
        plugin_result: list[str] = []
        plugin = part.plugin
        if plugin:
            plugin_result.append(plugin.type)
            if plugin.type not in ("module", "role", "playbook"):
                plugin_result.append(" plugin")
            plugin_result.append(
                f" :ref:`{rst_escape(plugin.fqcn)}"
                f" <ansible_collections.{plugin.fqcn}_{plugin.type}>`"
            )
        entrypoint = part.entrypoint
        if entrypoint is not None:
            if plugin_result:
                plugin_result.append(", ")
            plugin_result.append("entrypoint ")
            plugin_result.append(
                rst_escape(
                    entrypoint, escape_ending_whitespace=True, must_not_be_empty=True
                )
            )
        plugin_text = f" (of {''.join(plugin_result)})" if plugin_result else ""
        value_text = part.name
        value = part.value
        if value is not None:
            value_text = f"{value_text}={value}"
        escaped_text = rst_escape(
            value_text, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :literal:`{escaped_text}`{plugin_text}\\ "

    def format_error(self, part: dom.ErrorPart) -> str:
        text = rst_escape(
            part.message, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :strong:`ERROR while parsing`\\ : {text}\\ "

    def format_bold(self, part: dom.BoldPart) -> str:
        text = rst_escape(
            part.text, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :strong:`{text}`\\ "

    def format_code(self, part: dom.CodePart) -> str:
        text = rst_escape(
            part.text, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :literal:`{text}`\\ "

    def format_horizontal_line(self, part: dom.HorizontalLinePart) -> str:
        return "\n\n------------\n\n"

    def format_italic(self, part: dom.ItalicPart) -> str:
        text = rst_escape(
            part.text, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :emphasis:`{text}`\\ "

    def format_link(self, part: dom.LinkPart) -> str:
        if not part.text:
            return ""
        if not part.url:
            return rst_escape(part.text)
        text = rst_escape(part.text, escape_ending_whitespace=True)
        return f"\\ `{text} <{_url_escape(part.url)}>`__\\ "

    def format_module(self, part: dom.ModulePart, url: str | None) -> str:
        text = rst_escape(
            part.fqcn, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :ref:`{text} <ansible_collections.{part.fqcn}_module>`\\ "

    def format_rst_ref(self, part: dom.RSTRefPart) -> str:
        text = rst_escape(
            part.text, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :ref:`{text} <{part.ref}>`\\ "

    def format_url(self, part: dom.URLPart) -> str:
        if not part.url:
            return ""
        url_text = rst_escape(part.url, escape_ending_whitespace=True)
        return f"\\ `{url_text} <{_url_escape(part.url)}>`__\\ "

    def format_text(self, part: dom.TextPart) -> str:
        return rst_escape(part.text)

    def format_env_variable(self, part: dom.EnvVariablePart) -> str:
        text = rst_escape(
            part.name, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :envvar:`{text}`\\ "

    def format_option_name(self, part: dom.OptionNamePart, url: str | None) -> str:
        return self._format_option_like(part)

    def format_option_value(self, part: dom.OptionValuePart) -> str:
        text = rst_escape(
            part.value, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :literal:`{text}`\\ "

    def format_plugin(self, part: dom.PluginPart, url: str | None) -> str:
        return (
            f"\\ :ref:`{rst_escape(part.plugin.fqcn)} "
            f"<ansible_collections.{part.plugin.fqcn}_{part.plugin.type}>`\\ "
        )

    def format_return_value(self, part: dom.ReturnValuePart, url: str | None) -> str:
        return self._format_option_like(part)


DEFAULT_ANTSIBULL_FORMATTER = AntsibullRSTFormatter()
DEFAULT_PLAIN_FORMATTER = PlainRSTFormatter()

_BACKSLASH_SPACE_REPEAT = re.compile("\\\\ (?:\\\\ )+")
_BACKSLASH_SPACE_REMOVER_PRE = re.compile("(?<![\\\\])([ ])\\\\ (?![`])")
_BACKSLASH_SPACE_REMOVER_POST = re.compile("(?<!:`)\\\\ ([ .])")


def _remove_backslash_space(line: str) -> str:
    start = 0
    end = len(line)

    while True:
        # Remove starting '\ '. These have no effect.
        while line.startswith(r"\ ", start, end):
            start += 2

        # If the line now starts with regular whitespace, trim it.
        if line.startswith(" ", start, end):
            start += 1
        else:
            # If there is none, we're done.
            break

        # Remove more leading whitespace, and then check again for leading '\ ' etc.
        while line.startswith(" ", start, end):
            start += 1

    while True:
        # Remove trailing '\ ' resp. '\' (after line.strip()). These actually have an effect,
        # since they remove the linebreak. *But* if our markup generator emits '\ ' followed
        # by a line break, we still want the line break to count, so this is actually fixing
        # a bug.
        if line.endswith("\\", start, end):
            end -= 1
        while line.endswith(r"\ ", start, end):
            end -= 2

        # If the line now ends with regular whitespace, trim it.
        if line.endswith(" ", start, end):
            end -= 1
        else:
            # If there is none, we're done.
            break

        # Remove more ending whitespace, and then check again for trailing '\' etc.
        while line.endswith(" ", start, end):
            end -= 1

    # Return subset of the line
    line = line[start:end]
    line = _BACKSLASH_SPACE_REPEAT.sub("\\\\ ", line)
    line = _BACKSLASH_SPACE_REMOVER_POST.sub("\\1", line)
    line = _BACKSLASH_SPACE_REMOVER_PRE.sub("\\1", line)
    return line


def _check_line(index: int, lines: list[str], line: str) -> bool:
    if index < 0 or index >= len(lines):
        return False
    return lines[index] == line


def _modify_line(index: int, line: str, lines: list[str]) -> bool:
    raw_html = ".. raw:: html"
    dashes = "------------"
    hr = "  <hr>"
    if line not in ("", raw_html, dashes, hr):
        return True
    if line in (raw_html, dashes):
        return False
    if line == hr and _check_line(index - 2, lines, raw_html):
        return False
    if line == "" and (
        _check_line(index + 1, lines, raw_html)
        or _check_line(index - 1, lines, raw_html)
        or _check_line(index - 3, lines, raw_html)
    ):
        return False
    if line == "" and (
        _check_line(index + 1, lines, dashes) or _check_line(index - 1, lines, dashes)
    ):
        return False
    return True


def postprocess_rst_paragraph(par: str) -> str:
    lines = par.strip().splitlines()
    lines = [
        (
            _remove_backslash_space(line.strip().replace("\t", " "))
            if _modify_line(index, line, lines)
            else line
        )
        for index, line in enumerate(lines)
    ]
    lines = [
        line
        for index, line in enumerate(lines)
        if line or not _modify_line(index, line, lines)
    ]
    return "\n".join(lines)


def to_rst(
    paragraphs: t.Sequence[dom.Paragraph],
    formatter: Formatter = DEFAULT_ANTSIBULL_FORMATTER,
    link_provider: LinkProvider | None = None,
    par_start: str = "",
    par_end: str = "",
    par_sep: str = "\n\n",
    par_empty: str = "\\",
    current_plugin: dom.PluginIdentifier | None = None,
) -> str:
    return _format_paragraphs(
        paragraphs,
        formatter=formatter,
        link_provider=link_provider,
        par_start=par_start,
        par_end=par_end,
        par_sep=par_sep,
        par_empty=par_empty,
        current_plugin=current_plugin,
        postprocess_paragraph=postprocess_rst_paragraph,
    )


def to_rst_plain(
    paragraphs: t.Sequence[dom.Paragraph],
    formatter: Formatter = DEFAULT_PLAIN_FORMATTER,
    link_provider: LinkProvider | None = None,
    par_start: str = "",
    par_end: str = "",
    par_sep: str = "\n\n",
    par_empty: str = "\\",
    current_plugin: dom.PluginIdentifier | None = None,
) -> str:
    return _format_paragraphs(
        paragraphs,
        formatter=formatter,
        link_provider=link_provider,
        par_start=par_start,
        par_end=par_end,
        par_sep=par_sep,
        par_empty=par_empty,
        current_plugin=current_plugin,
        postprocess_paragraph=postprocess_rst_paragraph,
    )
