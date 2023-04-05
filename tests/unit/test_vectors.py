# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project

import typing as t

import pytest
import yaml

from antsibull_docs_parser import dom
from antsibull_docs_parser.ansible_doc_text import to_ansible_doc_text
from antsibull_docs_parser.format import LinkProvider
from antsibull_docs_parser.html import to_html, to_html_plain
from antsibull_docs_parser.md import to_md
from antsibull_docs_parser.parser import Context, parse
from antsibull_docs_parser.rst import to_rst, to_rst_plain

from .vectors import (
    VECTORS_FILE,
    get_ansible_doc_text_opts,
    get_context_parse_opts,
    get_html_opts_link_provider,
    get_md_opts_link_provider,
    get_rst_opts,
)

_SafeLoader: t.Any
try:
    # use C version if possible for speedup
    from yaml import CSafeLoader as _SafeLoader
except ImportError:
    from yaml import SafeLoader as _SafeLoader


def load_yaml_file(path: str) -> t.Any:
    with open(path, "rb") as stream:
        return yaml.load(stream, Loader=_SafeLoader)


TEST_DATA = sorted(load_yaml_file(VECTORS_FILE)["test_vectors"].items())


@pytest.mark.parametrize(
    "test_name, test_data",
    TEST_DATA,
    ids=[test_name for test_name, test_data in TEST_DATA],
)
def test_vectors(test_name: str, test_data: t.Mapping[str, t.Any]) -> None:
    context, parse_opts = get_context_parse_opts(test_data)
    parsed = parse(test_data["source"], context, **parse_opts)

    ansible_doc_text_opts = get_ansible_doc_text_opts(test_data)
    html_opts, html_link_provider = get_html_opts_link_provider(test_data)
    md_opts, md_link_provider = get_md_opts_link_provider(test_data)
    rst_opts = get_rst_opts(test_data)

    if "html" in test_data:
        result = to_html(parsed, link_provider=html_link_provider, **html_opts)
        assert result == test_data["html"]

    if "html_plain" in test_data:
        result = to_html_plain(parsed, link_provider=html_link_provider, **html_opts)
        assert result == test_data["html_plain"]

    if "md" in test_data:
        result = to_md(parsed, link_provider=md_link_provider, **md_opts)
        assert result == test_data["md"]

    if "rst" in test_data:
        result = to_rst(parsed, **rst_opts)
        assert result == test_data["rst"]

    if "rst_plain" in test_data:
        result = to_rst_plain(parsed, **rst_opts)
        assert result == test_data["rst_plain"]

    if "ansible_doc_text" in test_data:
        result = to_ansible_doc_text(parsed, **ansible_doc_text_opts)
        assert result == test_data["ansible_doc_text"]
