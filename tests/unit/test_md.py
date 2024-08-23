# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project

from antsibull_docs_parser import dom
from antsibull_docs_parser.md import md_escape, postprocess_md_paragraph, to_md


def test_md_escape():
    assert md_escape("") == ""
    assert md_escape("  foo  ") == "  foo  "
    assert (
        md_escape(r"[]!.()-\@<>?[]!.()-\@<>?&")
        == r"\[\]\!\.\(\)\-\\\@\<\>\?\[\]\!\.\(\)\-\\\@\<\>\?\&"
    )


def test_postprocess_md_paragraph():
    assert postprocess_md_paragraph("") == ""
    assert postprocess_md_paragraph(" \n foo \n\r\n \n\tbar \n ") == "foo\nbar"


def test_to_md():
    assert to_md([]) == ""
    assert to_md([[dom.TextPart(text="test")]]) == "test"
