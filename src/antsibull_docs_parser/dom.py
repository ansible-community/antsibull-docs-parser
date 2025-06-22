# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
DOM classes used by parser.
"""

from __future__ import annotations

import abc
import typing as t
from enum import Enum
from typing import NamedTuple

ErrorType = t.Union[t.Literal["ignore"], t.Literal["message"], t.Literal["exception"]]


class PluginIdentifier(NamedTuple):
    """
    A plugin identifier.
    """

    fqcn: str
    """The plugin's FQCN (fully qualified collection name)."""

    type: str
    """The plugin's type. Can also be ``"module"`` or ``"role"``."""


class PartType(Enum):
    """
    Identifies a part class.
    """

    ERROR = 0
    BOLD = 1
    CODE = 2
    HORIZONTAL_LINE = 3
    ITALIC = 4
    LINK = 5
    MODULE = 6
    RST_REF = 7
    URL = 8
    TEXT = 9
    ENV_VARIABLE = 10
    OPTION_NAME = 11
    OPTION_VALUE = 12
    PLUGIN = 13
    RETURN_VALUE = 14


class TextPart(NamedTuple):
    """
    Represents arbitrary unformatted (plain) text.
    """

    text: str
    """The unformatted text."""

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.TEXT] = PartType.TEXT
    """The type of this part."""


class ItalicPart(NamedTuple):
    """
    Represents some text formatted in italics.
    """

    text: str
    """The text to render in italics."""

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.ITALIC] = PartType.ITALIC
    """The type of this part."""


class BoldPart(NamedTuple):
    """
    Represents some text formatted in bold.
    """

    text: str
    """The text to render in bold."""

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.BOLD] = PartType.BOLD
    """The type of this part."""


class ModulePart(NamedTuple):
    """
    Represents an Ansible module reference.
    """

    fqcn: str
    """The module's FQCN (fully qualified collection name)."""

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.MODULE] = PartType.MODULE
    """The type of this part."""


class PluginPart(NamedTuple):
    """
    Represents an Ansible plugin reference.
    This also covers modules, roles, and playbooks.
    """

    plugin: PluginIdentifier
    """The plugin."""

    entrypoint: str | None  # can be present if plugin.type == "role"
    """In case the plugin is a role, this can be an entrypoint of that role."""

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.PLUGIN] = PartType.PLUGIN
    """The type of this part."""


class URLPart(NamedTuple):
    """
    Represents an URL without a title.
    """

    url: str
    """The URL."""

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.URL] = PartType.URL
    """The type of this part."""


class LinkPart(NamedTuple):
    """
    Represents an URL with a title.
    """

    text: str
    """The link's title."""

    url: str
    """The link's URL."""

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.LINK] = PartType.LINK
    """The type of this part."""


class RSTRefPart(NamedTuple):
    """
    Represents a reference to a ReStructuredText label in a Sphinx docsite.
    Most renderers simply reproduce the link's title (the text).
    """

    text: str
    """The reference's title."""

    ref: str
    """The RST (ReStructuredText) reference for the Sphinx Ansible docsite."""

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.RST_REF] = PartType.RST_REF
    """The type of this part."""


class CodePart(NamedTuple):
    """
    Represents "code" formatted text.
    """

    text: str
    """The text to render as code."""

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.CODE] = PartType.CODE
    """The type of this part."""


class OptionNamePart(NamedTuple):
    """
    References an option name, optionally with reference to the plugin,
    a role entrypoint (if the plugin is a role), link information, and a value.
    """

    plugin: PluginIdentifier | None
    """The (optional) plugin this option belongs to."""

    entrypoint: str | None  # present iff plugin.type == 'role'
    """The (optional) role's entry point this option belongs to."""

    link: list[str]
    """
    The option's name split up as a sequence of strings.

    For example, ``foo.bar[].baz`` will result in ``["foo", "bar", "baz"]``.
    """

    name: str
    """The option's name."""

    value: str | None
    """The (optional) option's value."""

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.OPTION_NAME] = PartType.OPTION_NAME


class OptionValuePart(NamedTuple):
    """
    References an Ansible value.
    """

    value: str
    """The value."""

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.OPTION_VALUE] = PartType.OPTION_VALUE
    """The type of this part."""


class EnvVariablePart(NamedTuple):
    """
    References an environment variable.
    """

    name: str
    """The environment variable's name."""

    value: str | None
    """The (optional) environment variable's value."""

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.ENV_VARIABLE] = PartType.ENV_VARIABLE
    """The type of this part."""


class ReturnValuePart(NamedTuple):
    """
    References an return value name, optionally with reference to the plugin,
    a role entrypoint (if the plugin is a role), link information, and a value.
    """

    plugin: PluginIdentifier | None
    """The (optional) plugin this return value belongs to."""

    entrypoint: str | None  # present iff plugin.type == 'role'
    """The (optional) role's entry point this return value belongs to."""

    link: list[str]
    """
    The return value's name split up as a sequence of strings.

    For example, ``foo.bar[].baz`` will result in ``["foo", "bar", "baz"]``.
    """

    name: str
    """The return value's name."""

    value: str | None
    """The (optional) return value's value."""

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.RETURN_VALUE] = PartType.RETURN_VALUE
    """The type of this part."""


class HorizontalLinePart(NamedTuple):
    """
    References a HTML `<hr>` tag.
    """

    source: str | None = None
    """The (optional) source of the markup."""

    type: t.Literal[PartType.HORIZONTAL_LINE] = PartType.HORIZONTAL_LINE
    """The type of this part."""


class ErrorPart(NamedTuple):
    """
    References a parsing error.

    The parser can ignore errors, raise them as exceptions,
    or emit them as error parts into the output. `ErrorPart` is used in the third case.
    """

    message: str
    """The error message."""

    source: str | None = None
    """The (optional) source of the markup that caused the error."""

    type: t.Literal[PartType.ERROR] = PartType.ERROR
    """The type of this part."""


AnyPart = t.Union[
    TextPart,
    ItalicPart,
    BoldPart,
    ModulePart,
    PluginPart,
    URLPart,
    LinkPart,
    RSTRefPart,
    CodePart,
    OptionNamePart,
    OptionValuePart,
    EnvVariablePart,
    ReturnValuePart,
    HorizontalLinePart,
    ErrorPart,
]
"""Type for a part class."""


Paragraph = list[AnyPart]
"""A paragraph is a sequence of parts."""


class Walker(abc.ABC):
    """
    Abstract base class for walker whose methods will be called for parts of a paragraph.
    """

    @abc.abstractmethod
    def process_error(self, part: ErrorPart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_bold(self, part: BoldPart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_code(self, part: CodePart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_horizontal_line(self, part: HorizontalLinePart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_italic(self, part: ItalicPart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_link(self, part: LinkPart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_module(self, part: ModulePart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_rst_ref(self, part: RSTRefPart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_url(self, part: URLPart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_text(self, part: TextPart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_env_variable(self, part: EnvVariablePart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_option_name(self, part: OptionNamePart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_option_value(self, part: OptionValuePart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_plugin(self, part: PluginPart) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def process_return_value(self, part: ReturnValuePart) -> None:
        pass  # pragma: no cover


class NoopWalker(Walker):
    """
    Concrete base class for walker whose methods will be called for parts of a paragraph.
    The default implementation for every part will not do anything.
    """

    def process_error(self, part: ErrorPart) -> None:
        pass

    def process_bold(self, part: BoldPart) -> None:
        pass

    def process_code(self, part: CodePart) -> None:
        pass

    def process_horizontal_line(self, part: HorizontalLinePart) -> None:
        pass

    def process_italic(self, part: ItalicPart) -> None:
        pass

    def process_link(self, part: LinkPart) -> None:
        pass

    def process_module(self, part: ModulePart) -> None:
        pass

    def process_rst_ref(self, part: RSTRefPart) -> None:
        pass

    def process_url(self, part: URLPart) -> None:
        pass

    def process_text(self, part: TextPart) -> None:
        pass

    def process_env_variable(self, part: EnvVariablePart) -> None:
        pass

    def process_option_name(self, part: OptionNamePart) -> None:
        pass

    def process_option_value(self, part: OptionValuePart) -> None:
        pass

    def process_plugin(self, part: PluginPart) -> None:
        pass

    def process_return_value(self, part: ReturnValuePart) -> None:
        pass


# pylint:disable-next=too-many-branches
def walk(paragraph: Paragraph, walker: Walker) -> None:  # noqa: C901
    """
    Call the corresponding methods of a walker object for every part of the paragraph.
    """
    for part in paragraph:
        if part.type == PartType.ERROR:
            walker.process_error(t.cast(ErrorPart, part))
        elif part.type == PartType.BOLD:
            walker.process_bold(t.cast(BoldPart, part))
        elif part.type == PartType.CODE:
            walker.process_code(t.cast(CodePart, part))
        elif part.type == PartType.HORIZONTAL_LINE:
            walker.process_horizontal_line(t.cast(HorizontalLinePart, part))
        elif part.type == PartType.ITALIC:
            walker.process_italic(t.cast(ItalicPart, part))
        elif part.type == PartType.LINK:
            walker.process_link(t.cast(LinkPart, part))
        elif part.type == PartType.MODULE:
            walker.process_module(t.cast(ModulePart, part))
        elif part.type == PartType.RST_REF:
            walker.process_rst_ref(t.cast(RSTRefPart, part))
        elif part.type == PartType.URL:
            walker.process_url(t.cast(URLPart, part))
        elif part.type == PartType.TEXT:
            walker.process_text(t.cast(TextPart, part))
        elif part.type == PartType.ENV_VARIABLE:
            walker.process_env_variable(t.cast(EnvVariablePart, part))
        elif part.type == PartType.OPTION_NAME:
            walker.process_option_name(t.cast(OptionNamePart, part))
        elif part.type == PartType.OPTION_VALUE:
            walker.process_option_value(t.cast(OptionValuePart, part))
        elif part.type == PartType.PLUGIN:
            walker.process_plugin(t.cast(PluginPart, part))
        elif part.type == PartType.RETURN_VALUE:
            walker.process_return_value(t.cast(ReturnValuePart, part))
        else:
            raise RuntimeError(f"Internal error: unknown type {part.type!r}")
