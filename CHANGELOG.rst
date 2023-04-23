=================================================================================================
antsibull-docs-parser -- Python library for processing Ansible documentation markup Release Notes
=================================================================================================

.. contents:: Topics


v0.4.0
======

Release Summary
---------------

Feature and bugfix release.

Minor Changes
-------------

- Adjust URL escaping to be more similar to JavaScript's ``encodeURI()`` (https://github.com/ansible-community/antsibull-docs-parser/pull/24).
- Also escape ``.`` in MarkDown (https://github.com/ansible-community/antsibull-docs-parser/pull/24).

Bugfixes
--------

- Fix URL escaping in MarkDown (https://github.com/ansible-community/antsibull-docs-parser/pull/24).

v0.3.0
======

Release Summary
---------------

Feature release.

Minor Changes
-------------

- Add support for plain RST rendering (https://github.com/ansible-community/antsibull-docs-parser/pull/20).

v0.2.0
======

Release Summary
---------------

New major release that increases compatibility with the `TypeScript code in antsibull-docs-ts <https://github.com/ansible-community/antsibull-docs-ts>`__.

Minor Changes
-------------

- Add strict mode for parsing (https://github.com/ansible-community/antsibull-docs-parser/pull/15).
- Add support for ansible-doc like text output (https://github.com/ansible-community/antsibull-docs-parser/pull/17).
- Add support for semantic markup in roles (https://github.com/ansible-community/antsibull-docs-parser/pull/9).
- Allow to add markup source to every paragraph part (https://github.com/ansible-community/antsibull-docs-parser/pull/18).
- Can switch between error messages containing a shortened version of the faulty markup or the full faulty markup command (https://github.com/ansible-community/antsibull-docs-parser/pull/19).
- Create script to update/extend the test vectors automatically (https://github.com/ansible-community/antsibull-docs-parser/pull/16).

Breaking Changes / Porting Guide
--------------------------------

- All DOM named tuples now have a ``source`` entry before ``type`` (https://github.com/ansible-community/antsibull-docs-parser/pull/18).
- By default, the error messages now contain the full faulty markup command (https://github.com/ansible-community/antsibull-docs-parser/pull/19).
- Extend ``OptionNamePart`` and ``ReturnValuePart`` named tuples by adding ``entrypoint`` after ``plugin`` (https://github.com/ansible-community/antsibull-docs-parser/pull/9).
- Modify ``LinkProvider.plugin_option_like_link`` signature to include a new argument ``entrypoint`` after ``plugin`` (https://github.com/ansible-community/antsibull-docs-parser/pull/9).
- ``CommandParser.parse`` has a new ``source`` parameter (https://github.com/ansible-community/antsibull-docs-parser/pull/18).

v0.0.1
======

Release Summary
---------------

Initial experimental release.
