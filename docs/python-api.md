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

## The internal representation

The classes making up the internal representation can be found in the `antsibull_docs_parser.dom` module. This module also provides basic functionality to process markup.

TODO

## Parsing Ansible markup

The parser can be found in the Python module `antsibull_docs_parser.parse`.

TODO

## Rendering Ansible markup

antsibull-docs-parser provides multiple Python packages for formatting:

* a general formatting framework in `antsibull_docs_parser.format`;
* a specific formatter for `ansible-doc` like plaintext formatting in `antsibull_docs_parser.ansible_doc_text`;
* customizable [HTML](https://en.wikipedia.org/wiki/HTML) rendering in `antsibull_docs_parser.html`;
* customizable [MarkDown](https://en.wikipedia.org/wiki/Markdown) rendering in `antsibull_docs_parser.md`;
* customizable [ReStructured Text](https://en.wikipedia.org/wiki/ReStructuredText) rendering in `antsibull_docs_parser.rst`;

### General formatting

TODO

### Ansible-doc like plaintext formatting

TODO

### HTML rendering

TODO

### MarkDown rendering

TODO

### ReStructuredText rendering

TODO
