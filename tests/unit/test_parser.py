# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project

import typing as t

import pytest

from antsibull_docs_parser import dom
from antsibull_docs_parser.parser import (
    CommandParser,
    Context,
    Parser,
    Whitespace,
    _process_whitespace,
    parse,
)

PROCESS_WHITESPACE_DATA: t.List[t.Tuple[str, bool, bool, str, str]] = [
    (
        "",
        False,
        False,
        "",
        "",
    ),
    (
        " ",
        False,
        False,
        " ",
        " ",
    ),
    (
        "  ",
        False,
        False,
        " ",
        " ",
    ),
    (
        "\n",
        False,
        False,
        " ",
        "\n",
    ),
    (
        "\n",
        False,
        True,
        " ",
        " ",
    ),
    (
        " \n ",
        False,
        False,
        " ",
        "\n",
    ),
    (
        "Foo \n\r\t\n\r Bar",
        False,
        False,
        "Foo Bar",
        "Foo\nBar",
    ),
]


@pytest.mark.parametrize(
    "text, code_environment, no_newlines, result_strip, result_keep_single_newlines",
    PROCESS_WHITESPACE_DATA,
)
def test__process_whitespace(
    text, code_environment, no_newlines, result_strip, result_keep_single_newlines
):
    res_strip = _process_whitespace(
        text,
        whitespace=Whitespace.STRIP,
        code_environment=code_environment,
        no_newlines=no_newlines,
    )
    print(repr(res_strip))
    assert res_strip == result_strip

    res_keep_single_newlines = _process_whitespace(
        text,
        whitespace=Whitespace.KEEP_SINGLE_NEWLINES,
        code_environment=code_environment,
        no_newlines=no_newlines,
    )
    print(repr(res_keep_single_newlines))
    assert res_keep_single_newlines == result_keep_single_newlines


TEST_PARSE_DATA: t.List[
    t.Tuple[
        t.Union[str, t.List[str]], Context, t.Dict[str, t.Any], t.List[dom.Paragraph]
    ]
] = [
    ("", Context(), {}, []),
    ([""], Context(), {}, [[]]),
    ("test", Context(), {}, [[dom.TextPart(text="test")]]),
    (
        "test",
        Context(),
        dict(add_source=True),
        [[dom.TextPart(text="test", source="test")]],
    ),
    # classic markup:
    (
        "foo I(bar) baz C( bam ) B( ( boo ) ) U(https://example.com/?foo=bar)HORIZONTALLINE L(foo ,  https://bar.com) R( a , b )M(foo.bar.baz)HORIZONTALLINEx M(foo.bar.baz.bam)",
        Context(),
        {},
        [
            [
                dom.TextPart(text="foo "),
                dom.ItalicPart(text="bar"),
                dom.TextPart(text=" baz "),
                dom.CodePart(text=" bam "),
                dom.TextPart(text=" "),
                dom.BoldPart(text=" ( boo "),
                dom.TextPart(text=" ) "),
                dom.URLPart(url="https://example.com/?foo=bar"),
                dom.HorizontalLinePart(),
                dom.LinkPart(text="foo", url="https://bar.com"),
                dom.TextPart(text=" "),
                dom.RSTRefPart(text=" a", ref="b "),
                dom.ModulePart(fqcn="foo.bar.baz"),
                dom.TextPart(text="HORIZONTALLINEx "),
                dom.ModulePart(fqcn="foo.bar.baz.bam"),
            ],
        ],
    ),
    (
        "foo I(bar) baz C( bam ) B( ( boo ) ) U(https://example.com/?foo=bar)HORIZONTALLINE L(foo ,  https://bar.com) R( a , b )M(foo.bar.baz)HORIZONTALLINEx M(foo.bar.baz.bam)",
        Context(),
        dict(add_source=True),
        [
            [
                dom.TextPart(text="foo ", source="foo "),
                dom.ItalicPart(text="bar", source="I(bar)"),
                dom.TextPart(text=" baz ", source=" baz "),
                dom.CodePart(text=" bam ", source="C( bam )"),
                dom.TextPart(text=" ", source=" "),
                dom.BoldPart(text=" ( boo ", source="B( ( boo )"),
                dom.TextPart(text=" ) ", source=" ) "),
                dom.URLPart(
                    url="https://example.com/?foo=bar",
                    source="U(https://example.com/?foo=bar)",
                ),
                dom.HorizontalLinePart(source="HORIZONTALLINE"),
                dom.LinkPart(
                    text="foo",
                    url="https://bar.com",
                    source="L(foo ,  https://bar.com)",
                ),
                dom.TextPart(text=" ", source=" "),
                dom.RSTRefPart(text=" a", ref="b ", source="R( a , b )"),
                dom.ModulePart(fqcn="foo.bar.baz", source="M(foo.bar.baz)"),
                dom.TextPart(text="HORIZONTALLINEx ", source="HORIZONTALLINEx "),
                dom.ModulePart(fqcn="foo.bar.baz.bam", source="M(foo.bar.baz.bam)"),
            ],
        ],
    ),
    (
        "foo I(bar) baz C( bam ) B( ( boo ) ) U(https://example.com/?foo=bar)HORIZONTALLINE L(foo ,  https://bar.com) R( a , b )M(foo.bar.baz)HORIZONTALLINEx M(foo.bar.baz.bam)",
        Context(),
        dict(only_classic_markup=True),
        [
            [
                dom.TextPart(text="foo "),
                dom.ItalicPart(text="bar"),
                dom.TextPart(text=" baz "),
                dom.CodePart(text=" bam "),
                dom.TextPart(text=" "),
                dom.BoldPart(text=" ( boo "),
                dom.TextPart(text=" ) "),
                dom.URLPart(url="https://example.com/?foo=bar"),
                dom.HorizontalLinePart(),
                dom.LinkPart(text="foo", url="https://bar.com"),
                dom.TextPart(text=" "),
                dom.RSTRefPart(text=" a", ref="b "),
                dom.ModulePart(fqcn="foo.bar.baz"),
                dom.TextPart(text="HORIZONTALLINEx "),
                dom.ModulePart(fqcn="foo.bar.baz.bam"),
            ],
        ],
    ),
    # semantic markup:
    (
        "foo E(a\\),b) P(foo.bar.baz#bam) baz V( b\\,\\na\\)\\\\m\\, ) O(foo) ",
        Context(),
        {},
        [
            [
                dom.TextPart(text="foo "),
                dom.EnvVariablePart(name="a),b"),
                dom.TextPart(text=" "),
                dom.PluginPart(
                    plugin=dom.PluginIdentifier(fqcn="foo.bar.baz", type="bam")
                ),
                dom.TextPart(text=" baz "),
                dom.OptionValuePart(value=" b,na)\\m, "),
                dom.TextPart(text=" "),
                dom.OptionNamePart(
                    plugin=None, entrypoint=None, link=["foo"], name="foo", value=None
                ),
                dom.TextPart(text=" "),
            ],
        ],
    ),
    (
        "foo E(a\\),b) P(foo.bar.baz#bam) baz V( b\\,\\na\\)\\\\m\\, ) O(foo) ",
        Context(),
        dict(add_source=True),
        [
            [
                dom.TextPart(text="foo ", source="foo "),
                dom.EnvVariablePart(name="a),b", source="E(a\\),b)"),
                dom.TextPart(text=" ", source=" "),
                dom.PluginPart(
                    plugin=dom.PluginIdentifier(fqcn="foo.bar.baz", type="bam"),
                    source="P(foo.bar.baz#bam)",
                ),
                dom.TextPart(text=" baz ", source=" baz "),
                dom.OptionValuePart(
                    value=" b,na)\\m, ", source="V( b\\,\\na\\)\\\\m\\, )"
                ),
                dom.TextPart(text=" ", source=" "),
                dom.OptionNamePart(
                    plugin=None,
                    entrypoint=None,
                    link=["foo"],
                    name="foo",
                    value=None,
                    source="O(foo)",
                ),
                dom.TextPart(text=" ", source=" "),
            ],
        ],
    ),
    # semantic markup option name:
    (
        "O(foo)",
        Context(),
        {},
        [
            [
                dom.OptionNamePart(
                    plugin=None, entrypoint=None, link=["foo"], name="foo", value=None
                ),
            ],
        ],
    ),
    (
        "O(ignore:foo)",
        Context(current_plugin=dom.PluginIdentifier("foo.bar.baz", type="bam")),
        {},
        [
            [
                dom.OptionNamePart(
                    plugin=None, entrypoint=None, link=["foo"], name="foo", value=None
                ),
            ],
        ],
    ),
    (
        "O(foo)",
        Context(current_plugin=dom.PluginIdentifier("foo.bar.baz", type="bam")),
        {},
        [
            [
                dom.OptionNamePart(
                    plugin=dom.PluginIdentifier("foo.bar.baz", type="bam"),
                    entrypoint=None,
                    link=["foo"],
                    name="foo",
                    value=None,
                ),
            ],
        ],
    ),
    (
        "O(foo.bar.baz#bam:foo)",
        Context(),
        {},
        [
            [
                dom.OptionNamePart(
                    plugin=dom.PluginIdentifier("foo.bar.baz", type="bam"),
                    entrypoint=None,
                    link=["foo"],
                    name="foo",
                    value=None,
                ),
            ],
        ],
    ),
    (
        "O(foo=bar)",
        Context(),
        {},
        [
            [
                dom.OptionNamePart(
                    plugin=None, entrypoint=None, link=["foo"], name="foo", value="bar"
                ),
            ],
        ],
    ),
    (
        "O(foo.baz=bam)",
        Context(),
        {},
        [
            [
                dom.OptionNamePart(
                    plugin=None,
                    entrypoint=None,
                    link=["foo", "baz"],
                    name="foo.baz",
                    value="bam",
                ),
            ],
        ],
    ),
    (
        "O(foo[1].baz[bam.bar.boing].boo)",
        Context(),
        {},
        [
            [
                dom.OptionNamePart(
                    plugin=None,
                    entrypoint=None,
                    link=["foo", "baz", "boo"],
                    name="foo[1].baz[bam.bar.boing].boo",
                    value=None,
                ),
            ],
        ],
    ),
    (
        "O(bar.baz.bam.boo#lookup:foo[1].baz[bam.bar.boing].boo)",
        Context(),
        {},
        [
            [
                dom.OptionNamePart(
                    plugin=dom.PluginIdentifier("bar.baz.bam.boo", type="lookup"),
                    entrypoint=None,
                    link=["foo", "baz", "boo"],
                    name="foo[1].baz[bam.bar.boing].boo",
                    value=None,
                ),
            ],
        ],
    ),
    # semantic markup return value name:
    (
        "RV(foo)",
        Context(),
        {},
        [
            [
                dom.ReturnValuePart(
                    plugin=None, entrypoint=None, link=["foo"], name="foo", value=None
                ),
            ],
        ],
    ),
    (
        "RV(ignore:foo)",
        Context(current_plugin=dom.PluginIdentifier("foo.bar.baz", type="bam")),
        {},
        [
            [
                dom.ReturnValuePart(
                    plugin=None, entrypoint=None, link=["foo"], name="foo", value=None
                ),
            ],
        ],
    ),
    (
        "RV(foo)",
        Context(current_plugin=dom.PluginIdentifier("foo.bar.baz", type="bam")),
        {},
        [
            [
                dom.ReturnValuePart(
                    plugin=dom.PluginIdentifier("foo.bar.baz", type="bam"),
                    entrypoint=None,
                    link=["foo"],
                    name="foo",
                    value=None,
                ),
            ],
        ],
    ),
    (
        "RV(foo.bar.baz#bam:foo)",
        Context(),
        {},
        [
            [
                dom.ReturnValuePart(
                    plugin=dom.PluginIdentifier("foo.bar.baz", type="bam"),
                    entrypoint=None,
                    link=["foo"],
                    name="foo",
                    value=None,
                ),
            ],
        ],
    ),
    (
        "RV(foo=bar)",
        Context(),
        {},
        [
            [
                dom.ReturnValuePart(
                    plugin=None, entrypoint=None, link=["foo"], name="foo", value="bar"
                ),
            ],
        ],
    ),
    (
        "RV(foo.baz=bam)",
        Context(),
        {},
        [
            [
                dom.ReturnValuePart(
                    plugin=None,
                    entrypoint=None,
                    link=["foo", "baz"],
                    name="foo.baz",
                    value="bam",
                ),
            ],
        ],
    ),
    (
        "RV(foo[1].baz[bam.bar.boing].boo)",
        Context(),
        {},
        [
            [
                dom.ReturnValuePart(
                    plugin=None,
                    entrypoint=None,
                    link=["foo", "baz", "boo"],
                    name="foo[1].baz[bam.bar.boing].boo",
                    value=None,
                ),
            ],
        ],
    ),
    (
        "RV(bar.baz.bam.boo#lookup:foo[1].baz[bam.bar.boing].boo)",
        Context(),
        {},
        [
            [
                dom.ReturnValuePart(
                    plugin=dom.PluginIdentifier("bar.baz.bam.boo", type="lookup"),
                    entrypoint=None,
                    link=["foo", "baz", "boo"],
                    name="foo[1].baz[bam.bar.boing].boo",
                    value=None,
                ),
            ],
        ],
    ),
    # bad parameter parsing (no escaping, error message):
    (
        "M(",
        Context(),
        dict(helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message='While parsing M() at index 1: Cannot find closing ")" after last parameter'
                )
            ],
        ],
    ),
    (
        "M(foo",
        Context(),
        dict(errors="message", helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message='While parsing M() at index 1: Cannot find closing ")" after last parameter'
                )
            ],
        ],
    ),
    (
        "L(foo)",
        Context(),
        dict(errors="message", helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message="While parsing L() at index 1: Cannot find comma separating parameter 1 from the next one"
                ),
            ],
        ],
    ),
    (
        "L(foo,bar",
        Context(),
        dict(errors="message", helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message='While parsing L() at index 1: Cannot find closing ")" after last parameter'
                )
            ],
        ],
    ),
    (
        "L(foo), bar",
        Context(),
        dict(errors="message", helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message='While parsing L() at index 1: Cannot find closing ")" after last parameter'
                )
            ],
        ],
    ),
    (
        "P(",
        Context(),
        dict(helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message='While parsing P() at index 1: Cannot find closing ")" after last parameter'
                )
            ],
        ],
    ),
    (
        "P(foo",
        Context(),
        dict(errors="message", helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message='While parsing P() at index 1: Cannot find closing ")" after last parameter'
                )
            ],
        ],
    ),
    # bad module ref (error message):
    (
        "M(foo)",
        Context(),
        dict(helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message='While parsing M() at index 1: Module name "foo" is not a FQCN'
                )
            ],
        ],
    ),
    (
        " M(foo.bar)",
        Context(),
        dict(errors="message", helpful_errors=False),
        [
            [
                dom.TextPart(text=" "),
                dom.ErrorPart(
                    message='While parsing M() at index 2: Module name "foo.bar" is not a FQCN'
                ),
            ],
        ],
    ),
    (
        "  M(foo. bar.baz)",
        Context(),
        dict(errors="message", helpful_errors=False),
        [
            [
                dom.TextPart(text="  "),
                dom.ErrorPart(
                    message='While parsing M() at index 3: Module name "foo. bar.baz" is not a FQCN'
                ),
            ],
        ],
    ),
    (
        "   M(foo) baz",
        Context(),
        dict(errors="message", helpful_errors=False),
        [
            [
                dom.TextPart(text="   "),
                dom.ErrorPart(
                    message='While parsing M() at index 4: Module name "foo" is not a FQCN'
                ),
                dom.TextPart(text=" baz"),
            ],
        ],
    ),
    # bad plugin ref (error message):
    (
        "P(foo)",
        Context(),
        dict(helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message='While parsing P() at index 1: Parameter "foo" is not of the form FQCN#type'
                ),
            ],
        ],
    ),
    (
        "P(f o.b r.b z#bar)",
        Context(),
        dict(errors="message", helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message='While parsing P() at index 1: Plugin name "f o.b r.b z" is not a FQCN'
                ),
            ],
        ],
    ),
    (
        "P(foo.bar.baz#b m)",
        Context(),
        dict(errors="message", helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message='While parsing P() at index 1: Plugin type "b m" is not valid'
                ),
            ],
        ],
    ),
    # bad option name/return value (error message):
    (
        "O(f o.b r.b z#bam:foobar)",
        Context(),
        dict(helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message='While parsing O() at index 1: Plugin name "f o.b r.b z" is not a FQCN'
                ),
            ],
        ],
    ),
    (
        "O(foo.bar.baz#b m:foobar)",
        Context(),
        dict(errors="message", helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message='While parsing O() at index 1: Plugin type "b m" is not valid'
                ),
            ],
        ],
    ),
    (
        "O(foo:bar:baz)",
        Context(),
        dict(errors="message", helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message='While parsing O() at index 1: Invalid option/return value name "foo:bar:baz"'
                ),
            ],
        ],
    ),
    (
        "O(foo.bar.baz#role:bam)",
        Context(),
        dict(errors="message", helpful_errors=False),
        [
            [
                dom.ErrorPart(
                    message="While parsing O() at index 1: Role reference is missing entrypoint"
                ),
            ],
        ],
    ),
    # bad parameter parsing (no escaping, ignore error):
    ("M(", Context(), dict(errors="ignore"), [[]]),
    ("M(foo", Context(), dict(errors="ignore", helpful_errors=True), [[]]),
    ("L(foo)", Context(), dict(errors="ignore", helpful_errors=False), [[]]),
    ("L(foo,bar", Context(), dict(errors="ignore"), [[]]),
    ("L(foo), bar", Context(), dict(errors="ignore"), [[]]),
    ("P(", Context(), dict(errors="ignore"), [[]]),
    ("P(foo", Context(), dict(errors="ignore"), [[]]),
    ("O(foo.bar.baz#role:bam)", Context(), dict(errors="ignore"), [[]]),
    # bad module ref (ignore error):
    ("M(foo)", Context(), dict(errors="ignore"), [[]]),
    (" M(foo.bar)", Context(), dict(errors="ignore"), [[dom.TextPart(text=" ")]]),
    (
        "  M(foo. bar.baz)",
        Context(),
        dict(errors="ignore"),
        [[dom.TextPart(text="  ")]],
    ),
    (
        "   M(foo) baz",
        Context(),
        dict(errors="ignore"),
        [
            [
                dom.TextPart(text="   "),
                dom.TextPart(text=" baz"),
            ],
        ],
    ),
    # bad plugin ref (ignore error):
    ("P(foo#bar)", Context(), dict(errors="ignore"), [[]]),
    ("P(f o.b r.b z#bar)", Context(), dict(errors="ignore"), [[]]),
    ("P(foo.bar.baz#b m)", Context(), dict(errors="ignore"), [[]]),
    # bad option name/return value (ignore error):
    ("O(f o.b r.b z#bam:foobar)", Context(), dict(errors="ignore"), [[]]),
    ("O(foo.bar.baz#b m:foobar)", Context(), dict(errors="ignore"), [[]]),
    ("O(foo:bar:baz)", Context(), dict(errors="ignore"), [[]]),
]


@pytest.mark.parametrize("paragraphs, context, kwargs, expected", TEST_PARSE_DATA)
def test_parse(
    paragraphs: t.Union[str, t.List[str]],
    context: Context,
    kwargs: t.Dict[str, t.Any],
    expected: t.List[dom.Paragraph],
) -> None:
    result = parse(paragraphs, context, **kwargs)
    print(result)
    assert result == expected


TEST_PARSE_THROW_DATA: t.List[
    t.Tuple[t.Union[str, t.List[str]], Context, t.Dict[str, t.Any], str]
] = [
    # bad parameter parsing (no escaping, throw error):
    (
        "M(",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing M() at index 1: Cannot find closing ")" after last parameter',
    ),
    (
        "M(foo",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing M() at index 1: Cannot find closing ")" after last parameter',
    ),
    (
        "L(foo)",
        Context(),
        dict(errors="exception", helpful_errors=False),
        "While parsing L() at index 1: Cannot find comma separating parameter 1 from the next one",
    ),
    (
        "L(foo,bar",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing L() at index 1: Cannot find closing ")" after last parameter',
    ),
    (
        "L(foo), bar",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing L() at index 1: Cannot find closing ")" after last parameter',
    ),
    (
        "P(",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing P() at index 1: Cannot find closing ")" after last parameter',
    ),
    (
        "P(foo",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing P() at index 1: Cannot find closing ")" after last parameter',
    ),
    # bad module ref (throw error):
    (
        "M(foo)",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing M() at index 1: Module name "foo" is not a FQCN',
    ),
    (
        " M(foo.bar)",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing M() at index 2: Module name "foo.bar" is not a FQCN',
    ),
    (
        "  M(foo. bar.baz)",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing M() at index 3: Module name "foo. bar.baz" is not a FQCN',
    ),
    (
        "   M(foo)",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing M() at index 4: Module name "foo" is not a FQCN',
    ),
    # bad plugin ref (throw error):
    (
        "P(foo)",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing P() at index 1: Parameter "foo" is not of the form FQCN#type',
    ),
    (
        "P(f o.b r.b z#bar)",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing P() at index 1: Plugin name "f o.b r.b z" is not a FQCN',
    ),
    (
        "P(foo.bar.baz#b m)",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing P() at index 1: Plugin type "b m" is not valid',
    ),
    # bad option name/return value (throw error):
    (
        "O(f o.b r.b z#bam:foobar)",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing O() at index 1: Plugin name "f o.b r.b z" is not a FQCN',
    ),
    (
        "O(foo.bar.baz#b m:foobar)",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing O() at index 1: Plugin type "b m" is not valid',
    ),
    (
        "O(foo:bar:baz)",
        Context(),
        dict(errors="exception", helpful_errors=False),
        'While parsing O() at index 1: Invalid option/return value name "foo:bar:baz"',
    ),
    (
        "O(foo.bar.baz#role:bam)",
        Context(),
        dict(errors="exception", helpful_errors=False),
        "While parsing O() at index 1: Role reference is missing entrypoint",
    ),
]


@pytest.mark.parametrize(
    "paragraphs, context, kwargs, exc_message", TEST_PARSE_THROW_DATA
)
def test_parse_bad(
    paragraphs: t.Union[str, t.List[str]],
    context: Context,
    kwargs: t.Dict[str, t.Any],
    exc_message: str,
) -> None:
    with pytest.raises(ValueError) as exc:
        parse(paragraphs, context, **kwargs)
    assert str(exc.value) == exc_message


TEST_TRIVIAL_PARSER = ["", "foo", "I(foo) B(bar) HORIZONTALLINE C(baz)"]


@pytest.mark.parametrize("input", TEST_TRIVIAL_PARSER)
def test_trivial_parser(input: str) -> None:
    parser = Parser([])
    result = parser.parse_string(input, Context())
    expected = [dom.TextPart(text=input)] if input else []
    assert result == expected
