# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
ReStructured Text serialization.
"""

import typing as t

from . import dom
from .format import Formatter, LinkProvider
from .format import format_paragraphs as _format_paragraphs
from .html import _url_escape


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

    if escape_ending_whitespace and value.endswith(" "):
        value = value + "\\ "
    if escape_ending_whitespace and value.startswith(" "):
        value = "\\ " + value
    if not value and must_not_be_empty:
        value = "\\ "

    return value


class AntsibullRSTFormatter(Formatter):
    @staticmethod
    def _format_option_like(
        part: t.Union[dom.OptionNamePart, dom.ReturnValuePart], role: str
    ) -> str:
        result: t.List[str] = []
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
        text = rst_escape(part.text, escape_ending_whitespace=True)
        return f"\\ `{text} <{_url_escape(part.url)}>`__\\ "

    def format_module(self, part: dom.ModulePart, url: t.Optional[str]) -> str:
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
        return f"\\ {_url_escape(part.url)}\\ "

    def format_text(self, part: dom.TextPart) -> str:
        return rst_escape(part.text)

    def format_env_variable(self, part: dom.EnvVariablePart) -> str:
        text = rst_escape(
            part.name, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :envvar:`{text}`\\ "

    def format_option_name(self, part: dom.OptionNamePart, url: t.Optional[str]) -> str:
        return self._format_option_like(part, "ansopt")

    def format_option_value(self, part: dom.OptionValuePart) -> str:
        text = rst_escape(
            part.value, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :ansval:`{text}`\\ "

    def format_plugin(self, part: dom.PluginPart, url: t.Optional[str]) -> str:
        return (
            f"\\ :ref:`{rst_escape(part.plugin.fqcn)} "
            f"<ansible_collections.{part.plugin.fqcn}_{part.plugin.type}>`\\ "
        )

    def format_return_value(
        self, part: dom.ReturnValuePart, url: t.Optional[str]
    ) -> str:
        return self._format_option_like(part, "ansretval")


class PlainRSTFormatter(Formatter):
    @staticmethod
    def _format_option_like(
        part: t.Union[dom.OptionNamePart, dom.ReturnValuePart],
    ) -> str:
        plugin_result: t.List[str] = []
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
        text = rst_escape(part.text, escape_ending_whitespace=True)
        return f"\\ `{text} <{_url_escape(part.url)}>`__\\ "

    def format_module(self, part: dom.ModulePart, url: t.Optional[str]) -> str:
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
        return f"\\ {_url_escape(part.url)}\\ "

    def format_text(self, part: dom.TextPart) -> str:
        return rst_escape(part.text)

    def format_env_variable(self, part: dom.EnvVariablePart) -> str:
        text = rst_escape(
            part.name, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :envvar:`{text}`\\ "

    def format_option_name(self, part: dom.OptionNamePart, url: t.Optional[str]) -> str:
        return self._format_option_like(part)

    def format_option_value(self, part: dom.OptionValuePart) -> str:
        text = rst_escape(
            part.value, escape_ending_whitespace=True, must_not_be_empty=True
        )
        return f"\\ :literal:`{text}`\\ "

    def format_plugin(self, part: dom.PluginPart, url: t.Optional[str]) -> str:
        return (
            f"\\ :ref:`{rst_escape(part.plugin.fqcn)} "
            f"<ansible_collections.{part.plugin.fqcn}_{part.plugin.type}>`\\ "
        )

    def format_return_value(
        self, part: dom.ReturnValuePart, url: t.Optional[str]
    ) -> str:
        return self._format_option_like(part)


DEFAULT_ANTSIBULL_FORMATTER = AntsibullRSTFormatter()
DEFAULT_PLAIN_FORMATTER = PlainRSTFormatter()


def to_rst(
    paragraphs: t.Sequence[dom.Paragraph],
    formatter: Formatter = DEFAULT_ANTSIBULL_FORMATTER,
    link_provider: t.Optional[LinkProvider] = None,
    par_start: str = "",
    par_end: str = "",
    par_sep: str = "\n\n",
    par_empty: str = r"\ ",
    current_plugin: t.Optional[dom.PluginIdentifier] = None,
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
    )


def to_rst_plain(
    paragraphs: t.Sequence[dom.Paragraph],
    formatter: Formatter = DEFAULT_PLAIN_FORMATTER,
    link_provider: t.Optional[LinkProvider] = None,
    par_start: str = "",
    par_end: str = "",
    par_sep: str = "\n\n",
    par_empty: str = r"\ ",
    current_plugin: t.Optional[dom.PluginIdentifier] = None,
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
    )
