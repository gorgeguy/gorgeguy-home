# Python outer-scope shadow scanner

This repo now contains a small standalone utility, [`py_shadow_scan.py`](/Users/jon/g/gorgeguy/gorgeguy-home/coding-tools/py_shadow_scan.py), that reports Python names which shadow bindings from an outer scope or earlier names in the same module.

## Existing tool that already does this

If you want an off-the-shelf linter, `pylint` already has this check:

- Rule: `W0621`
- Name: `redefined-outer-name`

That is the closest direct match I found for PyCharm's "Shadows name from outer scope" inspection.

## Usage

```bash
python3 py_shadow_scan.py path/to/file.py
python3 py_shadow_scan.py path/to/package_dir
python3 py_shadow_scan.py --mode module path/to/file.py
```

Example output:

```text
example.py:5: 'x' shadows assignment from module at line 1 inside function inner
```

Exit codes:

- `0`: no issues found
- `1`: one or more issues found
- `2`: no Python files found

## What it scans

The scanner is AST-based and dependency-free.

Modes:

- `lexical` (default): enclosing-scope shadowing, which matches the PyCharm warnings you showed
- `module`: broader same-file detection for earlier names in the same module

It currently reports shadowing for:

- function arguments
- assignments
- `for` loop targets
- `with ... as ...` targets
- `except ... as ...` targets
- imports
- implicit submodule bindings created in package `__init__.py` files
- function/class definitions
- lambda arguments
- comprehension variables

It ignores names declared `global` or `nonlocal` in the current scope.
