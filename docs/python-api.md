<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Python API

This page describes the Python API provided by the [antsibull-docs-parser Python package](https://pypi.org/project/antsibull-docs-parser/). The code can be found in the [antsibull-docs-parser GitHub repository](https://github.com/ansible-community/antsibull-docs-parser/).

The API is split into three parts:

1. Parsing Ansible markup.
1. Processing Ansible markup.
1. Rendering Ansible markup.

The library uses an internal representation of markup. This is basically a list of paragraphs, and every paragraph is a list of parts. Every part represents a piece of markup, including unformatted text. Parsing converts a string of Ansible markup into this internal representation. This internal representation can be modified or analyzed. Finally, rendering converts this internal representation back to strings in other markup languages, or as plain text with markup stripped.

## Complete example for parsing and rendering

The following code snippet parses a piece of Ansible markup and renders it in HTML:
```python
from antsibull_docs_parser.parser import parse
from antsibull_docs_parser.parser import Context, parse
from antsibull_docs_parser.html import to_html

input = "This is a B(simple) example of L(Ansible markup, https://docs.ansible.com/ansible/devel/dev_guide/ansible_markup.html)."
context = Context()
data = parse(input, context, strict=True)
print(to_html(data))
```

This prints:
```html
<p>This is a <b>simple</b> example of <a href='https://docs.ansible.com/ansible/devel/dev_guide/ansible_markup.html'>Ansible markup</a>.</p>
```

## The internal representation

The classes making up the internal representation can be found in the `antsibull_docs_parser.dom` module. This module also provides basic functionality to process markup.

### Parts

All the classes and data types mentioned in this section are part of `antsibull_docs_parser.dom`.

Every kind of part has its own class representing it. Every these classes has a property `type` of type `PartType`. The type `AnyPart` represents the union of all these classes, and `Paragraph` is a list of `AnyPart` objects.

Every part class has a `source` property, which is either a string or `None`. The parser allows to fill the markup's source into the parts. This can be useful when for example producing error messages during analysis, like when an invalid object is referenced.

* A `TextPart` represents arbitrary unformatted (plain) text.

    ```python
    class TextPart(NamedTuple):
        text: str
        source: str | None = None
        type: t.Literal[PartType.TEXT] = PartType.TEXT
    ```

* An `ItalicPart` represents some text formatted in italics.

    ```python
    class ItalicPart(NamedTuple):
        text: str
        source: str | None = None
        type: t.Literal[PartType.ITALIC] = PartType.ITALIC
    ```

* A `BoldPart` represents some text formatted in bold.

    ```python
    class BoldPart(NamedTuple):
        text: str
        source: str | None = None
        type: t.Literal[PartType.BOLD] = PartType.BOLD
    ```

* A `ModulePart` represents an Ansible module reference. The module is referenced by its Fully Qualified Collection Name (FQCN).

    ```python
    class ModulePart(NamedTuple):
        fqcn: str
        source: str | None = None
        type: t.Literal[PartType.MODULE] = PartType.MODULE
    ```

* A `PluginPart` represents an Ansible plugin reference. This also covers modules, roles, and playbooks. The plugin is referenced by its Fully Qualified Collection Name (FQCN) and its type.

    ```python
    class PluginIdentifier(NamedTuple):
        fqcn: str
        type: str

    class PluginPart(NamedTuple):
        plugin: PluginIdentifier
        source: str | None = None
        type: t.Literal[PartType.PLUGIN] = PartType.PLUGIN
    ```

* An `URLPart` represents an URL without a title.

    ```python
    class URLPart(NamedTuple):
        url: str
        source: str | None = None
        type: t.Literal[PartType.URL] = PartType.URL
    ```

* A `LinkPart` represents an URL with a title.

    ```python
    class LinkPart(NamedTuple):
        text: str
        url: str
        source: str | None = None
        type: t.Literal[PartType.LINK] = PartType.LINK
    ```

* A `RSTRefPart` represents a reference to a ReStructuredText label in a Sphinx docsite. Most renderers simply reproduce the link's title (the text).

    ```python
    class RSTRefPart(NamedTuple):
        text: str
        ref: str
        source: str | None = None
        type: t.Literal[PartType.RST_REF] = PartType.RST_REF
    ```

* A `CodePart` represents "code" formatted text.

    ```python
    class CodePart(NamedTuple):
        text: str
        source: str | None = None
        type: t.Literal[PartType.CODE] = PartType.CODE
    ```

* An `OptionNamePart` references an option name, optionally with reference to the plugin, a role entrypoint (if the plugin is a role), link information, and a value.

    ```python
    class OptionNamePart(NamedTuple):
        plugin: PluginIdentifier | None
        entrypoint: str | None  # present iff plugin.type == 'role'
        link: list[str]
        name: str
        value: str | None
        source: str | None = None
        type: t.Literal[PartType.OPTION_NAME] = PartType.OPTION_NAME
    ```

* An `OptionValuePart` references an option's value.

    ```python
    class OptionValuePart(NamedTuple):
        value: str
        source: str | None = None
        type: t.Literal[PartType.OPTION_VALUE] = PartType.OPTION_VALUE
    ```

* An `EnvVariablePart` references an environment variable.

    ```python
    class EnvVariablePart(NamedTuple):
        name: str
        source: str | None = None
        type: t.Literal[PartType.ENV_VARIABLE] = PartType.ENV_VARIABLE
    ```

* A `ReturnValuePart` references an return value name, optionally with reference to the plugin, a role entrypoint (if the plugin is a role), link information, and a value.

    ```python
    class ReturnValuePart(NamedTuple):
        plugin: PluginIdentifier | None
        entrypoint: str | None  # present iff plugin.type == 'role'
        link: list[str]
        name: str
        value: str | None
        source: str | None = None
        type: t.Literal[PartType.RETURN_VALUE] = PartType.RETURN_VALUE
    ```

* A `HorizontalLinePart` references a HTML `<hr>` tag.

    ```python
    class HorizontalLinePart(NamedTuple):
        source: str | None = None
        type: t.Literal[PartType.HORIZONTAL_LINE] = PartType.HORIZONTAL_LINE
    ```

* An `ErrorPart` references a parsing error. The parser can ignore errors, raise them as exceptions, or emit them as error parts into the output. `ErrorPart` is used in the third case.

    ```python
    class ErrorPart(NamedTuple):
        message: str
        source: str | None = None
        type: t.Literal[PartType.ERROR] = PartType.ERROR
    ```

### Walking parts

A **walker** is a class that provides a method for every part type. The `walk()` function will go through all parts of a paragraph and call the corresponding method of the walker for every part.

`antsibull_docs_parser.dom` provides two walker base classes:

* `Walker` is an abstract base class where every method is abstract and needs to be implemented. Use this if you want to be sure to handle every type, even if new types are added in the future.

* `NoopWalker` is a concrete base class where every method from `Walker` is implemented and does nothing by default. Use this if you only want to do something for some specific parts, and do not want to bother implementing all other required methods.

## Parsing Ansible markup

The parser can be found in the Python module `antsibull_docs_parser.parse`.

The parse function looks like this:
```python
def parse(
    text: str | t.Sequence[str],
    context: Context,
    errors: dom.ErrorType = "message",
    only_classic_markup: bool = False,
    strict: bool = False,
    add_source: bool = False,
    helpful_errors: bool = True,
    *,
    whitespace: Whitespace = Whitespace.IGNORE,
) -> list[dom.Paragraph]:
    ...
```

It takes a string (a single paragraph), or a sequence of strings (a list of paragraphs), and returns a list of paragraphs.

The parameters are as follows:

* `text: str | Sequence[str]` (**required**): A string or a sequence of strings. If given a sequence of strings, will assume that this is a list of paragraphs.
* `context: Context` (**required**): Contextual information. The `Context` class looks as follows:

    ```python
    class Context(t.NamedTuple):
        current_plugin: dom.PluginIdentifier | None = None
        role_entrypoint: str | None = None
    ```

    Set `current_plugin` if the Ansible markup is parsed in the context of a specific plugin, like when parsing a plugin's description, or the option and return value descriptions of a plugin. If a role's documentation is parsed, and the markup belongs to a specific entrypoint, you can also specify this entrypoint as `role_entrypoint`.

    This allows to automatically fill in this context in option and return value parts so it is clear which plugin's or role entrypoint's option or return value is referenced in case the markup does not specify the plugin resp. role entrypoint.

    Simply use an unmodified instance of `Context` when parsing general markup.

* `errors: "ignore" | "message" | "exception"` (default `message`): How to handle errors while parsing.

    `"ignore"` simply ignores errors.

    `"message"` inserts errors as `ErrorPart` parts into the output.

    `"exception"` makes the function throw Python exceptions. This also means that it will stop processing on the first error.

* `only_classic_markup: bool` (default `False`): Whether to ignore semantic markup and treat it as raw text.

    Should only be used in very special cases. This is mostly for backwards compatibility for processors that do not want to understand semantic markup.

* `strict: bool` (default `False`): Whether to be extra strict while parsing.

    Whether escaping should only be accepted if necessary. Only ever enable this when linting markup.

* `add_source: bool` (default `False`): Whether to add the source of every part to the part (`source` property).
* `helpful_errors: bool` (default `True`): Whether to include the faulty markup in error messages.
* `whitespace: IGNORE | STRIP | KEEP_SINGLE_NEWLINES` (default `IGNORE`): How to handle whitespace.

    * `Whitespace.IGNORE`: Keep all whitespace as-is.
    * `Whitespace.STRIP`: Reduce all whitespace (space, tabs, newlines, ...) to regular breakable or non-breakable spaces. Multiple spaces are kept in everything that's often rendered code-style, like `C()`, `O()`, `V()`, `RV()`, `E()`.
    * `Whitespace.KEEP_SINGLE_NEWLINES`: Similar to `Whitespace.STRIP`, but keep single newlines intact.

    In case the parsed markup is used to format output in a markup format that is whitespace sensitive, we recommend to use `Whitespace.STRIP` or `Whitespace.KEEP_SINGLE_NEWLINES`.

## Rendering Ansible markup

antsibull-docs-parser provides multiple Python packages for formatting:

* a general formatting framework in `antsibull_docs_parser.format`;
* a specific formatter for `ansible-doc` like plaintext formatting in `antsibull_docs_parser.ansible_doc_text`;
* customizable [HTML](https://en.wikipedia.org/wiki/HTML) rendering in `antsibull_docs_parser.html`;
* customizable [MarkDown](https://en.wikipedia.org/wiki/Markdown) rendering in `antsibull_docs_parser.md`;
* customizable [ReStructured Text](https://en.wikipedia.org/wiki/ReStructuredText) rendering in `antsibull_docs_parser.rst`;

### General formatting

`antsibull_docs_parser.format` provides two abstract base classes and one function:

* `LinkProvider` provides URLs for objects (plugins, options, and return values).
* `Formatter` converts parts to strings. URLs provided by the `LinkProvider` are also passed to the methods.
* `format_paragraphs` goes through one or multiple paragraphs, calls `LinkProvider` for parts that reference plugins, options, or return values, and passes the part together with potential URLs to the formatting methods of a `Formatter` object. The resulting strings are concatenated, with optional strings at the beginning of paragraphs, end of paragraphs, between paragraphs, and for empty paragraphs.

<!-- TODO: more details -->

### Ansible-doc like plaintext formatting

`antsibull_docs_parser.ansible_doc_text.to_ansible_doc_text()` converts one or multiple paragraphs into plain text, similar to `ansible-doc`'s text output.

<!-- TODO: more details -->

### HTML rendering

`antsibull_docs_parser.html` provides two functions for formatting HTML output:

* `to_html` formats one or multiple paragraphs as HTML output that is suited for use in Sphinx docsites.
* `to_plain_html` formats one or multiple paragraphs as plain HTML output.

These functions are customizable, and the formatters used can also be derived from to override formatting for specific parts.

<!-- TODO: more details -->

### MarkDown rendering

`antsibull_docs_parser.md` provides a function for formatting MarkDown output, `to_md`.

This function is customizable, and the formatter used can also be derived from to override formatting for specific parts.

<!-- TODO: more details -->

### ReStructuredText rendering

`antsibull_docs_parser.rst` provides two functions for formatting ReStructuredText output:

* `to_rst` formats one or multiple paragraphs as RST output that is suited for use in Sphinx docsites that use antsibull-docs' `sphinx_antsibull_ext` Sphinx extension.
* `to_rst_plain` formats one or multiple paragraphs as plain RST output.

These functions are customizable, and the formatters used can also be derived from to override formatting for specific parts.

<!-- TODO: more details -->
