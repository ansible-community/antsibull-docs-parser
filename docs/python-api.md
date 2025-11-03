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

::: antsibull_docs_parser.dom.PartType
    options:
      heading_level: 4
      members: false
::: antsibull_docs_parser.dom.AnyPart
    options:
      heading_level: 4
::: antsibull_docs_parser.dom.Paragraph
    options:
      heading_level: 4

Every part class has a `source` property, which is either a string or `None`. The parser allows to fill the markup's source into the parts. This can be useful when for example producing error messages during analysis, like when an invalid object is referenced.

* ::: antsibull_docs_parser.dom.TextPart
      options:
        # show_root_heading: false
        heading_level: 4

* ::: antsibull_docs_parser.dom.ItalicPart
      options:
        # show_root_heading: false
        heading_level: 4

* ::: antsibull_docs_parser.dom.BoldPart
      options:
        # show_root_heading: false
        heading_level: 4

* ::: antsibull_docs_parser.dom.ModulePart
      options:
        # show_root_heading: false
        heading_level: 4

* ::: antsibull_docs_parser.dom.PluginPart
      options:
        # show_root_heading: false
        heading_level: 4

    ::: antsibull_docs_parser.dom.PluginIdentifier
        options:
          # show_root_heading: false
          heading_level: 4

* ::: antsibull_docs_parser.dom.URLPart
      options:
        # show_root_heading: false
        heading_level: 4

* ::: antsibull_docs_parser.dom.LinkPart
      options:
        # show_root_heading: false
        heading_level: 4

* ::: antsibull_docs_parser.dom.RSTRefPart
      options:
        # show_root_heading: false
        heading_level: 4

* ::: antsibull_docs_parser.dom.CodePart
      options:
        # show_root_heading: false
        heading_level: 4

* ::: antsibull_docs_parser.dom.OptionNamePart
      options:
        # show_root_heading: false
        heading_level: 4

* ::: antsibull_docs_parser.dom.OptionValuePart
      options:
        # show_root_heading: false
        heading_level: 4

* ::: antsibull_docs_parser.dom.EnvVariablePart
      options:
        # show_root_heading: false
        heading_level: 4

* ::: antsibull_docs_parser.dom.ReturnValuePart
      options:
        # show_root_heading: false
        heading_level: 4

* ::: antsibull_docs_parser.dom.HorizontalLinePart
      options:
        # show_root_heading: false
        heading_level: 4

* ::: antsibull_docs_parser.dom.ErrorPart
      options:
        # show_root_heading: false
        heading_level: 4

### Walking parts

A **walker** is a class that provides a method for every part type. The `walk()` function will go through all parts of a paragraph and call the corresponding method of the walker for every part.

::: antsibull_docs_parser.dom.walk
    options:
      # show_root_heading: false
      heading_level: 4

`antsibull_docs_parser.dom` provides two walker base classes:

* `Walker` is an abstract base class where every method is abstract and needs to be implemented. Use this if you want to be sure to handle every type, even if new types are added in the future.

* `NoopWalker` is a concrete base class where every method from `Walker` is implemented and does nothing by default. Use this if you only want to do something for some specific parts, and do not want to bother implementing all other required methods.

::: antsibull_docs_parser.dom.Walker
    options:
      # show_root_heading: false
      heading_level: 4

::: antsibull_docs_parser.dom.NoopWalker
    options:
      # show_root_heading: false
      heading_level: 4

## Parsing Ansible markup

The parser can be found in the Python module `antsibull_docs_parser.parser`.

::: antsibull_docs_parser.parser.parse
    options:
      # show_root_heading: false
      heading_level: 4

::: antsibull_docs_parser.parser.Context
    options:
      # show_root_heading: false
      heading_level: 4

::: antsibull_docs_parser.parser.Whitespace
    options:
      # show_root_heading: false
      heading_level: 4

## Rendering Ansible markup

antsibull-docs-parser provides multiple Python packages for formatting:

* a general formatting framework in `antsibull_docs_parser.format`;
* a specific formatter for `ansible-doc` like plaintext formatting in `antsibull_docs_parser.ansible_doc_text`;
* customizable [HTML](https://en.wikipedia.org/wiki/HTML) rendering in `antsibull_docs_parser.html`;
* customizable [MarkDown](https://en.wikipedia.org/wiki/Markdown) rendering in `antsibull_docs_parser.md`; and
* customizable [ReStructured Text](https://en.wikipedia.org/wiki/ReStructuredText) rendering in `antsibull_docs_parser.rst`.

### General formatting

`antsibull_docs_parser.format` provides two abstract base classes and one function:

* `LinkProvider` provides URLs for objects (plugins, options, and return values).
* `Formatter` converts parts to strings. URLs provided by the `LinkProvider` are also passed to the methods.
* `format_paragraphs` goes through one or multiple paragraphs, calls `LinkProvider` for parts that reference plugins, options, or return values, and passes the part together with potential URLs to the formatting methods of a `Formatter` object. The resulting strings are concatenated, with optional strings at the beginning of paragraphs, end of paragraphs, between paragraphs, and for empty paragraphs.

::: antsibull_docs_parser.format.LinkProvider
    options:
      # show_root_heading: false
      heading_level: 4

::: antsibull_docs_parser.format.Formatter
    options:
      # show_root_heading: false
      heading_level: 4

::: antsibull_docs_parser.format.format_paragraphs
    options:
      # show_root_heading: false
      heading_level: 4

### Ansible-doc like plaintext formatting

`antsibull_docs_parser.ansible_doc_text.to_ansible_doc_text()` converts one or multiple paragraphs into plain text, similar to `ansible-doc`'s text output.

::: antsibull_docs_parser.ansible_doc_text.to_ansible_doc_text
    options:
      # show_root_heading: false
      heading_level: 4

### HTML rendering

`antsibull_docs_parser.html` provides two functions for formatting HTML output.
These functions are customizable, and the formatters used can also be derived from to override formatting for specific parts.

::: antsibull_docs_parser.html.to_html
    options:
      # show_root_heading: false
      heading_level: 4

::: antsibull_docs_parser.html.to_html_plain
    options:
      # show_root_heading: false
      heading_level: 4

### MarkDown rendering

`antsibull_docs_parser.md` provides a function for formatting MarkDown output, `to_md`.
This function is customizable, and the formatter used can also be derived from to override formatting for specific parts.

::: antsibull_docs_parser.md.to_md
    options:
      # show_root_heading: false
      heading_level: 4

### ReStructuredText rendering

`antsibull_docs_parser.rst` provides two functions for formatting ReStructuredText output.
These functions are customizable, and the formatters used can also be derived from to override formatting for specific parts.

::: antsibull_docs_parser.rst.to_rst
    options:
      # show_root_heading: false
      heading_level: 4

::: antsibull_docs_parser.rst.to_rst_plain
    options:
      # show_root_heading: false
      heading_level: 4
