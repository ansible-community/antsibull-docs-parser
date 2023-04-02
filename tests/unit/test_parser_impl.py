# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project

import typing as t

import pytest

from antsibull_docs_parser._parser_impl import (
    parse_parameters_escaped,
    parse_parameters_unescaped,
)

ESCAPED_TESTS = [
    ["(a)", 1, 1, False, ["a"], 3, None],
    ["(a,b)", 1, 1, False, ["a,b"], 5, None],
    ["(a,b,c)", 1, 1, False, ["a,b,c"], 7, None],
    ["(a,b)", 1, 2, False, ["a", "b"], 5, None],
    ["(a,b,c)", 1, 2, False, ["a", "b,c"], 7, None],
    ["(a,b,c)", 1, 3, False, ["a", "b", "c"], 7, None],
    ["(a\\,,b\\,\\),c\\))", 1, 3, False, ["a,", "b,)", "c)"], 15, None],
    ["(a\\\\,b\\),c\\)\\\\)", 1, 3, True, ["a\\", "b)", "c)\\"], 15, None],
    ["(a", 1, 1, False, [""], 2, 'Cannot find closing ")" after last parameter'],
    [
        "(a",
        1,
        2,
        False,
        [""],
        2,
        "Cannot find comma separating parameter 1 from the next one",
    ],
    ["(a,b", 1, 2, False, ["a", ""], 4, 'Cannot find closing ")" after last parameter'],
    ["(c\\a)", 1, 1, False, ["ca"], 5, None],
    ["(c\\a)", 1, 1, True, ["c"], 4, 'Unnecessarily escaped "a"'],
    ["(c\\a,b)", 1, 2, False, ["ca", "b"], 7, None],
    ["(c\\a,b)", 1, 2, True, ["c"], 4, 'Unnecessarily escaped "a"'],
]


@pytest.mark.parametrize(
    "text, index, parameter_count, strict, expected_result, expected_index, expected_error",
    ESCAPED_TESTS,
)
def test_parse_parameters_escaped(
    text: str,
    index: int,
    parameter_count: int,
    strict: bool,
    expected_result: t.List[str],
    expected_index: int,
    expected_error: t.Optional[str],
) -> None:
    result, end_index, error = parse_parameters_escaped(
        text, index, parameter_count, strict=strict
    )
    print(result, end_index, error)
    assert result == expected_result
    assert end_index == expected_index
    assert error == expected_error


UNESCAPED_TESTS = [
    ["(a)", 1, 1, False, ["a"], 3, None],
    ["(a,b)", 1, 1, False, ["a,b"], 5, None],
    ["(a,b,c)", 1, 1, False, ["a,b,c"], 7, None],
    ["(a,b)", 1, 2, False, ["a", "b"], 5, None],
    ["(a,b,c)", 1, 2, False, ["a", "b,c"], 7, None],
    ["(a,b,c)", 1, 3, False, ["a", "b", "c"], 7, None],
    ["(a", 1, 1, False, [], 2, 'Cannot find closing ")" after last parameter'],
    [
        "(a",
        1,
        2,
        False,
        [],
        2,
        "Cannot find comma separating parameter 1 from the next one",
    ],
    ["(a,b", 1, 2, False, ["a"], 4, 'Cannot find closing ")" after last parameter'],
]


@pytest.mark.parametrize(
    "text, index, parameter_count, strict, expected_result, expected_index, expected_error",
    UNESCAPED_TESTS,
)
def test_parse_parameters_unescaped(
    text: str,
    index: int,
    parameter_count: int,
    strict: bool,
    expected_result: t.List[str],
    expected_index: int,
    expected_error: t.Optional[str],
) -> None:
    result, end_index, error = parse_parameters_unescaped(
        text, index, parameter_count, strict=strict
    )
    print(result, end_index, error)
    assert result == expected_result
    assert end_index == expected_index
    assert error == expected_error
