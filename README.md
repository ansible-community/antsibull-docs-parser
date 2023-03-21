<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
SPDX-FileCopyrightText: 2023, Ansible Project
-->

# antsibull-docs-parser - Python library for processing Ansible documentation markup

[![NOX badge](https://github.com/ansible-community/antsibull-docs-parser/actions/workflows/nox.yml/badge.svg)](https://github.com/ansible-community/antsibull-docs-parser/actions/workflows/nox.yml)
[![Codecov badge](https://img.shields.io/codecov/c/github/ansible-community/antsibull-docs-parser)](https://codecov.io/gh/ansible-community/antsibull-docs-parser)

This is a Python library for processing Ansible documentation markup. It is named after [antsibull-docs](https://github.com/ansible-community/antsibull-docs/) where this code originates from. It was moved out to make it easier to reuse the markup code in other projects without having to depend on all of antsibull-docs's dependencies.

## Development

Install and run `nox` to run all tests. `nox` will create virtual environments in `.nox` inside the checked out project and install the requirements needed to run the tests there.

To run specific tests:
1. `nox -e test` to only run unit tests;
2. `nox -e lint` to run all linters and formatters at once;
3. `nox -e formatters` to run `isort`;
4. `nox -e codeqa` to run `flake8`, `pylint`, and `reuse lint`;
5. `nox -e typing` to run `mypy` and `pyre`.

## Releasing a new version

1. Update package version in `pyproject.toml`.
2. Run `nox -e bump -- <version> <release_summary_message>`. This does:
   * Create `changelogs/fragments/<version>.yml` with a `release_summary` section.
   * Run `antsibull-changelog release` and add the changed files to git.
   * Commit with message `Release <version>.` and run `git tag -a -m 'antsibull-docs-parser <version>' <version>`.
3. Run `git push upstream main && git push`.
4. Once CI passes on GitHub, run `nox -e publish`. This does:
   * Run `hatch publish`;
   * Run `git push --follow-tags`;
   * Bumps the version to `<version>.post0`;
   * Add the changed file to git and run `git commit -m 'Post-release version bump.'`;
5. Run `git push upstream main` and create a GitHub release;
