# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project

from antsibull_docs_parser import dom
from antsibull_docs_parser.ansible_doc_text import to_ansible_doc_text


def test_to_ansible_doc_text():
    assert to_ansible_doc_text([]) == ""
    assert to_ansible_doc_text([[dom.TextPart(text="test")]]) == "test"
