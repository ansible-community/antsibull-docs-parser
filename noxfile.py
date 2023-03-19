# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Maxwell G <maxwell@gtmx.me>

import os

import nox

IN_CI = "GITHUB_ACTIONS" in os.environ
ALLOW_EDITABLE = os.environ.get("ALLOW_EDITABLE", str(not IN_CI)).lower() in (
    "1",
    "true",
)

# Always install latest pip version
os.environ["VIRTUALENV_DOWNLOAD"] = "1"
nox.options.sessions = "lint", "test"


def install(session: nox.Session, *args, editable=False, **kwargs):
    # nox --no-venv
    if isinstance(session.virtualenv, nox.virtualenv.PassthroughEnv):
        session.warn(f"No venv. Skipping installation of {args}")
        return
    # Don't install in editable mode in CI or if it's explicitly disabled.
    # This ensures that the wheel contains all of the correct files.
    if editable and ALLOW_EDITABLE:
        args = ("-e", *args)
    session.install(*args, "-U", **kwargs)


@nox.session(python=["3.6", "3.7", "3.8", "3.9", "3.10", "3.11"])
def test(session: nox.Session):
    install(session, ".", "pytest", "pytest-cov", "pyyaml", editable=True)
    session.run(
        "pytest",
        "--cov-branch",
        "--cov=antsibull_docs_parser",
    )


@nox.session
def lint(session: nox.Session):
    session.notify("formatters")
    session.notify("codeqa")
    session.notify("typing")


@nox.session
def formatters(session: nox.Session):
    install(session, "isort")
    posargs = list(session.posargs)
    if IN_CI:
        posargs.append("--check")
    session.run("isort", *posargs, "src", "tests")


@nox.session
def codeqa(session: nox.Session):
    install(session, ".", "flake8", "pylint", "reuse", editable=True)
    session.run(
        "flake8",
        "--count",
        "--max-complexity=10",
        "--max-line-length=100",
        "--statistics",
        "src/antsibull_docs_parser",
        *session.posargs,
    )
    session.run(
        "pylint", "--rcfile", ".pylintrc.automated", "src/antsibull_docs_parser"
    )
    session.run("reuse", "lint")


@nox.session
def typing(session: nox.Session):
    install(session, ".", "mypy", "pyre-check", editable=True)
    session.run("mypy", "src/antsibull_docs_parser")
    session.run("pyre", "--source-directory", "src/antsibull_docs_parser")
