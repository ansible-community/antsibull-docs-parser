=================================================================================================
antsibull-docs-parser -- Python library for processing Ansible documentation markup Release Notes
=================================================================================================

.. contents:: Topics

v1.2.1
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Accept upper-case letters when validating FQCNs (https://github.com/ansible-community/antsibull-docs-parser/pull/71).

v1.2.0
======

Release Summary
---------------

Maintenance release that drops support for older Python releases.

Removed Features (previously deprecated)
----------------------------------------

- antsibull-docs-parser no longer supports Python 3.6, 3.7, and 3.8. Python 3.9+ is now required (https://github.com/ansible-community/antsibull-docs-parser/pull/68).

v1.1.1
======

Release Summary
---------------

Bugfix release.

Minor Changes
-------------

- Declare support for Python 3.13 (https://github.com/ansible-community/antsibull-docs-parser/pull/59).

Bugfixes
--------

- Make sure to also escape pipes (``\|``) in reStructured Text (https://github.com/ansible-community/antsibull-docs-parser/pull/65).

v1.1.0
======

Release Summary
---------------

Bugfix and feature release that improves markup parsing and generation with respect to whitespace handling and escaping.

Minor Changes
-------------

- Allow to determine how to handle whitespace during parsing with the new ``whitespace`` option (https://github.com/ansible-community/antsibull-docs-parser/pull/54).
- Always remove some whitespace around ``HORIZONTALLINE`` (https://github.com/ansible-community/antsibull-docs-parser/pull/54).
- Apply postprocessing to RST and MarkDown to avoid generating invalid markup when input contains whitespace at potentially dangerous places (https://github.com/ansible-community/antsibull-docs-parser/pull/56).

Bugfixes
--------

- Do not apply URI encoding to visible URL (https://github.com/ansible-community/antsibull-docs-parser/pull/53).
- Fix RST escaping to handle other whitespace than spaces correctly (https://github.com/ansible-community/antsibull-docs-parser/pull/56).
- Improve handling of empty URL for links (https://github.com/ansible-community/antsibull-docs-parser/pull/53).

v1.0.2
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Fix handling of empty markup parameters for RST (https://github.com/ansible-community/antsibull-docs-parser/pull/51).

v1.0.1
======

Release Summary
---------------

Maintenance release.

Minor Changes
-------------

- Declare support for Python 3.12 (https://github.com/ansible-community/antsibull-docs-parser/pull/45).

Bugfixes
--------

- Properly escape MarkDown link targets (https://github.com/ansible-community/antsibull-docs-parser/pull/37).

v1.0.0
======

Release Summary
---------------

First stable release. This package is using semantic versioning, so there will be no more breaking changes until the release of 2.0.0.

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
