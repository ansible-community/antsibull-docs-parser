# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project

import typing as t

import yaml
from vectors import (
    VECTORS_FILE,
    get_ansible_doc_text_opts,
    get_context_parse_opts,
    get_html_opts_link_provider,
    get_md_opts_link_provider,
    get_rst_opts,
)
from yaml.representer import SafeRepresenter

from antsibull_docs_parser.ansible_doc_text import to_ansible_doc_text
from antsibull_docs_parser.html import to_html, to_html_plain
from antsibull_docs_parser.md import to_md
from antsibull_docs_parser.parser import parse
from antsibull_docs_parser.rst import to_rst, to_rst_plain


class LiteralString(str):
    pass


def change_style(style, representer):
    def new_representer(dumper, data):
        scalar = representer(dumper, data)
        scalar.style = style
        return scalar

    return new_representer


represent_literal_str = change_style("|", SafeRepresenter.represent_str)


yaml.add_representer(LiteralString, represent_literal_str)


def add(test_data: t.Dict[str, t.Any], key: str, value: t.Any) -> None:
    if isinstance(value, str) and value:
        if "\r" in value or "\t" in value:
            pass
        elif "\n" in value:
            value = LiteralString(value)
        elif value == value.rstrip(" "):
            value = LiteralString(value)
    test_data[key] = value


def update(test_name: str, test_data: t.Dict[str, t.Any]) -> None:
    context, parse_opts = get_context_parse_opts(test_data)
    parsed = parse(test_data["source"], context, **parse_opts)

    ansible_doc_text_opts = get_ansible_doc_text_opts(test_data)
    html_opts, html_link_provider = get_html_opts_link_provider(test_data)
    md_opts, md_link_provider = get_md_opts_link_provider(test_data)
    rst_opts = get_rst_opts(test_data)

    result = to_html(parsed, link_provider=html_link_provider, **html_opts)
    add(test_data, "html", result)

    result = to_html_plain(parsed, link_provider=html_link_provider, **html_opts)
    add(test_data, "html_plain", result)

    result = to_md(parsed, link_provider=md_link_provider, **md_opts)
    add(test_data, "md", result)

    result = to_rst(parsed, **rst_opts)
    add(test_data, "rst", result)

    result = to_rst_plain(parsed, **rst_opts)
    add(test_data, "rst_plain", result)

    result = to_ansible_doc_text(parsed, **ansible_doc_text_opts)
    add(test_data, "ansible_doc_text", result)


class IndentedDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def main() -> None:
    with open(VECTORS_FILE, "r") as stream:
        data = yaml.load(stream, Loader=yaml.Loader)

    for test_name, test_data in data["test_vectors"].items():
        update(test_name, test_data)

    with open(VECTORS_FILE, "w") as stream:
        stream.write(
            r"""---
# Simplified BSD License (see LICENSES/BSD-2-Clause.txt or https://opensource.org/licenses/BSD-2-Clause)
# SPDX-FileCopyrightText: Ansible Project
# SPDX-License-Identifier: BSD-2-Clause

"""
        )
        stream.write(
            yaml.dump(
                data,
                Dumper=IndentedDumper,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )
        )


if __name__ == "__main__":
    main()
