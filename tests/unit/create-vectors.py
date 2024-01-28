# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project

import typing as t

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from vectors import (
    VECTORS_FILE,
    get_ansible_doc_text_opts,
    get_context_parse_opts,
    get_html_opts_link_provider,
    get_md_opts_link_provider,
    get_rst_opts,
)

from antsibull_docs_parser.ansible_doc_text import to_ansible_doc_text
from antsibull_docs_parser.html import to_html, to_html_plain
from antsibull_docs_parser.md import to_md
from antsibull_docs_parser.parser import parse
from antsibull_docs_parser.rst import to_rst, to_rst_plain


def add(test_data: t.Dict[str, t.Any], key: str, value: t.Any) -> None:
    if isinstance(value, str):
        if "\n" in value:
            value = LiteralScalarString(value)
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


def main() -> None:
    yaml = YAML(typ="rt")
    with open(VECTORS_FILE, "r") as stream:
        data = yaml.load(stream)

    for test_name, test_data in data["test_vectors"].items():
        update(test_name, test_data)

    yaml = YAML()
    yaml.default_flow_style = False
    yaml.explicit_start = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    with open(VECTORS_FILE, "w") as stream:
        yaml.dump(data, stream)


if __name__ == "__main__":
    main()
