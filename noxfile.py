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
    session.run("pyre", "--source-directory", "src")


def _repl_version(session: nox.Session, new_version: str):
    with open("pyproject.toml", "r+") as fp:
        lines = tuple(fp)
        fp.seek(0)
        for line in lines:
            if line.startswith("version = "):
                line = f'version = "{new_version}"\n'
            fp.write(line)


@nox.session
def bump(session: nox.Session):
    version = session.posargs[0]
    install(session, "antsibull-changelog")
    _repl_version(session, version)
    if len(session.posargs) > 1:
        with open(f"changelogs/fragments/{version}.yml", "w") as fp:
            print("release_summary:", session.posargs[1], file=fp)
    session.run("antsibull-changelog", "release")
    session.run("git", "add", "CHANGELOG.rst", "changelogs/changelog.yaml", "changelogs/fragments/", external=True)
    install(session, ".")  # Smoke test
    session.run("git", "commit", "-m", f"Release {version}.", external=True)
    session.run(
        "git",
        "tag",
        "-a",
        "-m",
        f"antsibull-docs-parser {version}",
        "--edit",
        version,
        external=True,
    )


@nox.session
def publish(session: nox.Session):
    install(session, "hatch")
    session.run("hatch", "publish", *session.posargs)
    session.run("git", "push", "--follow-tags")
    version = session.run("hatch", "version", silent=True).strip()
    _repl_version(session, f"{version}.post0")
    session.run("git", "commit", "pyproject.toml")
    session.run("git", "commit", "-m", "Post-release version bump.", external=True)
