# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project

import typing as t

from antsibull_docs_parser import dom
from antsibull_docs_parser.format import LinkProvider
from antsibull_docs_parser.html import to_html, to_html_plain
from antsibull_docs_parser.md import to_md
from antsibull_docs_parser.parser import Context, parse
from antsibull_docs_parser.rst import to_rst

VECTORS_FILE = "test-vectors.yaml"


class _TestLinkProvider(LinkProvider):
    _plugin_link = None
    _plugin_option_like_link = None

    def plugin_link(self, plugin: dom.PluginIdentifier) -> t.Optional[str]:
        if self._plugin_link is not None:
            return self._plugin_link(plugin)
        return None

    def plugin_option_like_link(
        self,
        plugin: dom.PluginIdentifier,
        entrypoint: t.Optional[str],
        what: "t.Union[t.Literal['option'], t.Literal['retval']]",
        name: t.List[str],
        current_plugin: bool,
    ) -> t.Optional[str]:
        if self._plugin_option_like_link is not None:
            return self._plugin_option_like_link(
                plugin, entrypoint, what, name, current_plugin
            )
        return None

    def _update(self, config: t.Mapping[str, t.Any]):
        if "pluginLink.py" in config:
            self._plugin_link = eval(config["pluginLink.py"])
        if "pluginOptionLikeLink.py" in config:
            self._plugin_option_like_link = eval(config["pluginOptionLikeLink.py"])


def get_context_parse_opts(test_data: t.Mapping[str, t.Any]):
    parse_opts = {}
    context_opts = {}
    if test_data.get("parse_opts"):
        if "current_plugin" in test_data["parse_opts"]:
            context_opts["current_plugin"] = dom.PluginIdentifier(
                fqcn=test_data["parse_opts"]["current_plugin"]["fqcn"],
                type=test_data["parse_opts"]["current_plugin"]["type"],
            )
        if "role_entrypoint" in test_data["parse_opts"]:
            context_opts["role_entrypoint"] = test_data["parse_opts"]["role_entrypoint"]
        if "errors" in test_data["parse_opts"]:
            parse_opts["errors"] = test_data["parse_opts"]["errors"]
        if "onlyClassicMarkup" in test_data["parse_opts"]:
            parse_opts["only_classic_markup"] = test_data["parse_opts"][
                "onlyClassicMarkup"
            ]
        if "helpfulErrors" in test_data["parse_opts"]:
            parse_opts["helpful_errors"] = test_data["parse_opts"]["helpfulErrors"]
    return Context(**context_opts), parse_opts


def get_html_opts_link_provider(test_data: t.Mapping[str, t.Any]):
    opts = {}
    link_provider = _TestLinkProvider()
    if test_data.get("html_opts"):
        if "parStart" in test_data["html_opts"]:
            opts["par_start"] = test_data["html_opts"]["parStart"]
        if "parEnd" in test_data["html_opts"]:
            opts["par_end"] = test_data["html_opts"]["parEnd"]
        if "current_plugin" in test_data["html_opts"]:
            opts["current_plugin"] = dom.PluginIdentifier(
                fqcn=test_data["html_opts"]["current_plugin"]["fqcn"],
                type=test_data["html_opts"]["current_plugin"]["type"],
            )
        link_provider._update(test_data["html_opts"])
    return opts, link_provider


def get_md_opts_link_provider(test_data: t.Mapping[str, t.Any]):
    opts = {}
    link_provider = _TestLinkProvider()
    if test_data.get("md_opts"):
        if "current_plugin" in test_data["md_opts"]:
            opts["current_plugin"] = dom.PluginIdentifier(
                fqcn=test_data["md_opts"]["current_plugin"]["fqcn"],
                type=test_data["md_opts"]["current_plugin"]["type"],
            )
        link_provider._update(test_data["md_opts"])
    return opts, link_provider


def get_rst_opts(test_data: t.Mapping[str, t.Any]):
    opts = {}
    if test_data.get("rst_opts"):
        if "current_plugin" in test_data["rst_opts"]:
            opts["current_plugin"] = dom.PluginIdentifier(
                fqcn=test_data["rst_opts"]["current_plugin"]["fqcn"],
                type=test_data["rst_opts"]["current_plugin"]["type"],
            )
    return opts


def get_ansible_doc_text_opts(test_data: t.Mapping[str, t.Any]):
    opts = {}
    if test_data.get("ansible_doc_text_opts"):
        if "current_plugin" in test_data["ansible_doc_text_opts"]:
            opts["current_plugin"] = dom.PluginIdentifier(
                fqcn=test_data["ansible_doc_text_opts"]["current_plugin"]["fqcn"],
                type=test_data["ansible_doc_text_opts"]["current_plugin"]["type"],
            )
    return opts
