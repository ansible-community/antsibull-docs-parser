<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Ansible Markup Specification

This document provides a specification of Ansible markup. An informal specification more concerned with *using* the markup can be found [on the Ansible docsite](https://docs.ansible.com/ansible/devel/dev_guide/ansible_markup.html).

## History and overview

Ansible markup is a simple formatting language that is primarily used to document Ansible modules and plugins. It can be roughly split into two parts:

1. **Classical Ansible markup.** This was the original markup, and allowed to apply basic formatting.
    The only semantic information was referencing Ansible modules with `M(...)`.
    Parsing was done with simple regular expressions;
    in particular it was not possible to use escaping, for example to use a closing bracket in formatting.

    By convention, particular formatting was used to denote semantic information, like italics were used for option names, and code formatting for values.
    Unfortunately authors not always agreed on these semantics, so some modules used italics for values and code formatting for option names.
    For that reason, in 2021 the Documentation Working Group (DaWGs) [discussed to extend Ansible markup by semantic elements](https://github.com/ansible/ansible/pull/73137).
    Unfortunately, it took several years to convince all stakeholders that this should go forward.

1. **Semantic markup.** In 2023, the markup language was extended by more *semantic* elements that allow to denote and reference plugins, option names, return value names, values, environment variables, etc. The new elements allow escaping of letters like commas and closing brackets.

To ease implementation of Ansible markup in different tools, two libraries were created:

1. [antsibull-docs-parser for Python](https://github.com/ansible-community/antsibull-docs-parser/);
1. [antsibull-docs-ts for TypeScript/JavaScript](https://github.com/ansible-community/antsibull-docs-ts).

These libraries aim to have no other dependencies, and provide a generic API to parse, process, and format Ansible markup.
They are used by most Ansible markup processors, like [antsibull-docs](https://github.com/ansible-community/antsibull-docs/), Ansible Galaxy's documentation renderer, and the [Ansible VS Code extension](https://github.com/ansible/vscode-ansible).

## Markup elements

Basically Ansible markup consists of plain text that uses formatting directives. These directives start with upper-case letters, are followed by `(` in case they have parameters, followed by one or more parameters as plain text, separated by commas (`,`), and terminated by a `)`.

For example, `Foo B(bar) L(baz, bam).` consists of the text `Foo `, the directive `B` (for bold) with parameter `bar`, the directive `L` (for link) with two parameters `baz` and `bam`, and the text `.`.

The opening bracket must follow the directive's name without spacing. The number of parameters is determined by the directive's name. For some directives, `,` and `)` can be escaped in parameters by using a backslash (`\`): the parameter for `V` in `V(foo(bar\))` is `foo(bar)`. The directive's name must be separated from previous text by a non-letter (word boundary).

The following directives are supported:

* `B` (one parameter; no escaping): bold text.
* `C` (one parameter; no escaping): code.
* `HR` (no parameters): horizontal line.
* `I` (one parameter; no escaping): italic text.
* `L` (two parameters; no escaping): link with title.
* `M` (one parameter; no escaping): module reference.
* `R` (one parameter; no escaping): ReStructuredText reference.
* `U` (one parameter; no escaping): URL (without title).
* `E` (one parameter; with escaping): environment variable.
* `O` (one parameter; with escaping): option name with optional value and plugin reference.
* `V` (one parameter; with escaping): Ansible value.
* `P` (one parameter; with escaping): plugin reference.
* `RV` (one parameter; with escaping): return value wiht optional value and plugin reference.

Depending on the markup element, the parameters must have a special form, respectively will be parsed further.

### Text formatting

For `B(...)`, `C(...)`, and `I(...)`, the parameter can be anything (that does not contain a closing bracket, `)`).

### Web links

The `U(...)` markup describes a single URL without a title. The `L(..., ...)` markup describes a URL with a title ("link"); the first parameter is the title, the second the URL.

### Module and plugin references

Module references `M(...)` use FQCNs (fully qualified collection names) to reference modules in collections. The collection name `ansible.builtin` is used for modules included with ansible-core.

Plugin references `P(...)` must have a parameter of the form `fqcn#type`, where `fqcn` is the FQCN of the plugin, and `type` the plugin's type. In case `type` is `role`, the form `fqcn#role:entrypoint` is allowed as well.

### ReStructuredText references

The `R(..., ...)` markup describes a [ReStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) reference. The first parameter is the reference's title, while the second parameter is the RST label.

Renderers that can not link to RST labels should simply show the title instead.

### Environment variable references

The `E(...)` markup's parameter is the name of an environment variable.

### Ansible values

For `V(...)`, the parameter can be anything, and even contain closing bracket by escaping with a backslash (`\`).

### Option and return value references

The syntax for `O(...)` and `RV(...)` is more complex, and identical. The general form is `(plugin.fqcn#type:|role.fqcn#role:entry_point:|ignore:)name(=value|)`.

The parameter is parsed as follows:

1. Split by the first `=`. If there is no `=`, then there is **no value**. Otherwise, everything right of `=` is the **value**.
1. The left side of `=` (or everything, if there was no `=`) is split by the last `:`. The last part is the **name**.
1. The part before the name is either empty, or one of the following:

    1. `ignore`: in that case, the option/return value name **does not reference to any concrete plugin/role's option resp. return value**.
    1. `fqcn#type`: in that case, the option/return value name does **belong to the plugin** with FQCN `fqcn` of type `type`.
       This is not valid if `type` is `"role"`; in that case, an entrypoint *must* be specified.
    1. `fqcn#role:entrypoint`: in that case, the option/return value name does **belong to the role** with FQCN `fqcn`'s entrypoint `entrypoint`.
       `role` must be the literal text `"role"`.
