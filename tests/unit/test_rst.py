# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project

from antsibull_docs_parser import dom
from antsibull_docs_parser.rst import (
    postprocess_rst_paragraph,
    rst_escape,
    to_rst,
    to_rst_plain,
)


def test_rst_escape():
    assert rst_escape("") == ""
    assert rst_escape("  foo  ") == "  foo  "
    assert rst_escape("  foo  ", True) == "\\   foo  \\ "
    assert rst_escape("\\<_>`*<_>*`\\|") == "\\\\\\<\\_\\>\\`\\*\\<\\_\\>\\*\\`\\\\\\|"


def test_postprocess_rst_paragraph():
    assert postprocess_rst_paragraph("") == ""
    assert postprocess_rst_paragraph(" \n foo \n\r\n \n\tbar \n ") == "foo\nbar"
    assert (
        postprocess_rst_paragraph("\\ foo\\  \\  bar \\  \\ \n\nf\\ oo")
        == "foo  bar\nf\\ oo"
    )
    assert postprocess_rst_paragraph("a\\ \\ \\ \\ \\ b") == "a\\ b"
    assert postprocess_rst_paragraph("a\\ \\  \\ \\    \\ \\  ") == "a"
    assert postprocess_rst_paragraph("\\ \\  \\ \\    \\ \\  a") == "a"
    assert postprocess_rst_paragraph("\\ \\  \\ \\    \\ \\  ") == ""


def test_to_rst():
    assert to_rst([]) == ""
    assert to_rst([[dom.TextPart(text="test")]]) == "test"


def test_to_rst_plain():
    assert to_rst_plain([]) == ""
    assert to_rst_plain([[dom.TextPart(text="test")]]) == "test"
