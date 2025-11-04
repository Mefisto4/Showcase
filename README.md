# Showcase - example project

---

## Purpose

Purpose of this project is to give quick and overall view of some of my skills in the recruitment processes.

---

## .venv

This project bases on virtual environment. In PowerShell, change your directory to this project main directory (.
/Showcase/), then create a virtual environment `.venv`:

`>> python -m venv .venv` (sometimes, you may need to provide full path to python interpreter)

Activate it:

`>> .\.venv\Scripts\activate.bat`

You should notice a change at the beginning of command prompt. Instead of this:

`PS >>`

You should see this:

`(.venv) PS >>`

What means you have activated your virtual environment successfully.

Finally, you need to install required packages:

`>> pip install -r requirements.txt`

Once you're done working with this project, deactivate the venv:

`>> deactivate`

You should see `PS >>` without (.venv) once again.

P.S. If you made any changes to the required packages (added new ones or upgraded existing ones), you can update
requirements.txt with the following command, **while still working in .venv**:

`>> pip freeze > requirements.txt`

---

## pre-commit hooks

To ensure high-quality contributions, pre-commit hooks are configured. You need to install them:

`>> pre-commit install`

Then, you can check if everything is working fine:

`>> pre-commit run --all-files`

Pre-commit hook runs `ruff` against files with matching extension to lint and format them.

P.S. It also advised to run `pylint` and `mypy` checkers on all changed files before committing them.

---

## GitHub workflows

There are 2 configured workflows, that are being executed whenever:

- a `push` is made to any branch, or
- a `pull_request` event is triggered.

These workflows run ruff linter and formatter and pylint checker.

---

## Linters, checkers, formatters

This project uses the following tools:

1. [ruff - "An extremely fast Python linter and code formatter, written in Rust."](https://docs.astral.sh/ruff)
    - configuration file: `./pyproject.toml`
2. [pylint - a static code analyser](https://pylint.readthedocs.io/en/stable)
    - configuration file: `./.pylintrc`
3. [mypy - a static type checker](https://mypy.readthedocs.io/en/stable)

---

## Coverage check

It is possible to measure code coverage using [Coverage.py](https://coverage.readthedocs.io/en/7.11.0).

To use it,
replace command initial `python` with `coverage run`:

- `python something.py` becomes `coverage run something.py`
- `python -m amodule` becomes `coverage run -m amodule`

In this test framework, you can measure code coverage by simply using:

- `coverage run -m pytest .\tests\test_control_objects_unit_tests.py`

Then, to see the report:

- `coverage report -m` - to see the report in CLI
- `coverage html` - to generate html file with the report

---

## PyTest

Tests have been written using `pytest` framework.

- pytest configuration file: `./pytest.ini`
- pytest fixtures file: `./conftest.py`

To run the tests, you can use one of the following options:

1. Simple run:
    - `>> pytest .\tests\`
2. Run based on marker (i.e. custom marker "unit"):
    - `>> pytest .\tests\ -m unit`
3. Run based on keywords (i.e. "TestLink"):
    - `>> pytest .\tests\ -k TestLink`
4. Distributed run (i.e. run all unit-tests distributed across multiple workers equal to number of available CPUs):
    - `>> pytest -n auto .\tests\ -m unit`

---
