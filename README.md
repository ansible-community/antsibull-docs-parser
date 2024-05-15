<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
SPDX-FileCopyrightText: 2023, Ansible Project
-->

# antsibull-docs-parser - Python library for processing Ansible documentation markup
[![Discuss on Matrix at #antsibull:ansible.com](https://img.shields.io/matrix/antsibull:ansible.com.svg?server_fqdn=ansible-accounts.ems.host&label=Discuss%20on%20Matrix%20at%20%23antsibull:ansible.com&logo=matrix)](https://matrix.to/#/#antsibull:ansible.com)
[![Nox badge](https://github.com/ansible-community/antsibull-docs-parser/actions/workflows/nox.yml/badge.svg)](https://github.com/ansible-community/antsibull-docs-parser/actions/workflows/nox.yml)
[![Codecov badge](https://img.shields.io/codecov/c/github/ansible-community/antsibull-docs-parser)](https://codecov.io/gh/ansible-community/antsibull-docs-parser)
[![REUSE status](https://api.reuse.software/badge/github.com/ansible-community/antsibull-docs-parser)](https://api.reuse.software/info/github.com/ansible-community/antsibull-docs-parser)

This is a Python library for processing Ansible documentation markup. It is named after [antsibull-docs](https://github.com/ansible-community/antsibull-docs/) where this code originates from. It was moved out to make it easier to reuse the markup code in other projects without having to depend on all of antsibull-docs's dependencies.

## Development

Install and run `nox` to run all tests. `nox` will create virtual environments in `.nox` inside the checked out project and install the requirements needed to run the tests there.

To run specific tests:
1. `nox -e test` to only run unit tests;
2. `nox -e lint` to run all linters and formatters at once;
3. `nox -e formatters` to run `isort` and `black`;
4. `nox -e codeqa` to run `flake8`, `pylint`, `reuse lint`, and `antsibull-changelog lint`;
5. `nox -e typing` to run `mypy` and `pyre`;
6. `nox -e create_vectors` to update the `test-vectors.yml` file. Please note that this file should be synchronized with the corresponding file in [the antsibull-docs-ts project](https://github.com/ansible-community/antsibull-docs-ts).

## Releasing a new version

1. Run `nox -e bump -- <version> <release_summary_message>`. This:
   * Bumps the package version in `src/antsibull_docs_parser/__init__.py`.
   * Creates `changelogs/fragments/<version>.yml` with a `release_summary` section.
   * Runs `antsibull-changelog release` and adds the changed files to git.
   * Commits with message `Release <version>.` and runs `git tag -a -m 'antsibull-docs-parser <version>' <version>`.
   * Runs `hatch build --clean`.
2. Run `git push` to the appropriate remotes.
3. Once CI passes on GitHub, run `nox -e publish`. This:
   * Runs `hatch publish`;
   * Bumps the version to `<version>.post0`;
   * Adds the changed file to git and run `git commit -m 'Post-release version bump.'`;
4. Run `git push --follow-tags` to the appropriate remotes and create a GitHub release.
