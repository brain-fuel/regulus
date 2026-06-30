# regulus Fork — v0.1.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up `regulus` — a hard fork of dbrattli/Expression renamed to the `regulus` namespace, retooled on uv/ruff/mypy, MIT-attributed, with the full upstream test suite green on Python 3.11/3.12.

**Architecture:** Vendor the upstream `expression/` package + `tests/` into the `python/regulus/` repo, mechanically rename the `expression` import namespace to `regulus`, replace Poetry tooling with a uv/hatchling `pyproject.toml`, and gate on ruff + pytest (mypy advisory for v0.1). No API changes — the public surface is byte-for-byte the upstream API under a new name.

**Tech Stack:** Python 3.11+, uv (env + build runner), hatchling (build backend), ruff (lint/format), mypy (type check, advisory), pytest + pytest-asyncio + hypothesis (tests).

## Global Constraints

- Python floor: **3.11+** (upstream was 3.10+; bump, no code change needed).
- License: **MIT**. Retain upstream `LICENSE` text verbatim; add `NOTICE` crediting `dbrattli/Expression`.
- Import package name: **`regulus`**. Distribution name: **`gf-regulus`**.
- **No API changes in v0.1** — rename only. Public symbols keep upstream names.
- Repo: `github.com/brain-fuel/regulus`; local path `goforge.dev/python/regulus`.
- Rename is import-scoped: replace `from expression`, `import expression`, and `expression.` only. The bare English word "expression" in docstrings stays.
- All commands run from the repo root `python/regulus/` unless stated. The repo is already `git init`'d and contains `docs/`.
- Upstream source to vendor lives at: `/tmp/claude-1000/-home-brainfuel-matt-goforge-dev/4e43a0c0-edf7-46ec-9e41-f0117742e34b/scratchpad/Expression` (shallow clone). If absent, re-clone: `git clone --depth 1 https://github.com/dbrattli/Expression.git <dir>`.

---

### Task 1: Vendor upstream source

**Files:**
- Create: `python/regulus/expression/` (full upstream package tree, renamed in Task 2)
- Create: `python/regulus/tests/` (full upstream test suite)
- Create: `python/regulus/LICENSE` (upstream MIT, verbatim)

**Interfaces:**
- Consumes: nothing.
- Produces: the raw upstream tree at `python/regulus/`, pre-rename. Later tasks rename and retool it.

- [ ] **Step 1: Copy the package, tests, and license from the clone**

```bash
SRC=/tmp/claude-1000/-home-brainfuel-matt-goforge-dev/4e43a0c0-edf7-46ec-9e41-f0117742e34b/scratchpad/Expression
DST=/home/brainfuel/matt/goforge.dev/python/regulus
cp -r "$SRC/expression" "$DST/expression"
cp -r "$SRC/tests" "$DST/tests"
cp "$SRC/LICENSE" "$DST/LICENSE"
```

- [ ] **Step 2: Verify the tree landed**

Run: `cd /home/brainfuel/matt/goforge.dev/python/regulus && ls expression tests LICENSE && ls expression/core | head`
Expected: `expression/` shows `__init__.py collections core effect extra py.typed system`; `tests/` shows the `test_*.py` files; `LICENSE` present; `expression/core` lists `option.py result.py pipe.py ...`.

- [ ] **Step 3: Commit**

```bash
cd /home/brainfuel/matt/goforge.dev/python/regulus
git add expression tests LICENSE
git commit -m "chore: vendor dbrattli/Expression source for regulus fork"
```

---

### Task 2: Rename the `expression` namespace to `regulus`

**Files:**
- Modify (rename): `expression/` → `regulus/`
- Modify: every `.py` under `regulus/` and `tests/` (import rewrite)
- Modify: `regulus/_version.py` (pin version)
- Modify: `regulus/__init__.py` (docstring + homepage URL)

**Interfaces:**
- Consumes: vendored tree from Task 1.
- Produces: an importable `regulus` package (`import regulus`, `from regulus.core import Option, Result, pipe`, …) with identical public symbols to upstream. No install yet — verified by compile + grep here; import is verified in Task 4.

- [ ] **Step 1: Rename the package directory**

```bash
cd /home/brainfuel/matt/goforge.dev/python/regulus
git mv expression regulus
```

- [ ] **Step 2: Rewrite import references across package + tests**

```bash
cd /home/brainfuel/matt/goforge.dev/python/regulus
grep -rlE 'from expression|import expression|expression\.' --include='*.py' regulus tests \
  | xargs sed -i \
      -e 's/from expression/from regulus/g' \
      -e 's/import expression/import regulus/g' \
      -e 's/expression\./regulus./g'
```

- [ ] **Step 3: Pin the version (drop dunamai dynamic versioning)**

Overwrite `regulus/_version.py` with exactly:

```python
__version__ = "0.1.0"
```

- [ ] **Step 4: Fix the package docstring + homepage in `regulus/__init__.py`**

Replace the module docstring (the top triple-quoted block ending in the `GitHub:` line) with exactly:

```python
"""regulus — practical functional programming for Python.

regulus is the pure, dross-free functional core of goforge's Python wing:
type-safe Option, Result, pipe, effects, tagged unions, and immutable
collections. A hard fork of dbrattli/Expression.

GitHub: https://github.com/brain-fuel/regulus
"""
```

- [ ] **Step 5: Verify no stray `expression` import references remain**

Run: `cd /home/brainfuel/matt/goforge.dev/python/regulus && grep -rnE 'from expression|import expression|expression\.' --include='*.py' regulus tests`
Expected: no output (exit 1 from grep — zero matches).

- [ ] **Step 6: Verify every module byte-compiles**

Run: `cd /home/brainfuel/matt/goforge.dev/python/regulus && python3 -m compileall -q regulus tests && echo COMPILE_OK`
Expected: `COMPILE_OK` (no syntax/compile errors).

- [ ] **Step 7: Commit**

```bash
cd /home/brainfuel/matt/goforge.dev/python/regulus
git add -A
git commit -m "refactor: rename expression namespace to regulus"
```

---

### Task 3: uv `pyproject.toml` + tooling configs

**Files:**
- Create: `python/regulus/pyproject.toml`
- Create: `python/regulus/.gitignore`

**Interfaces:**
- Consumes: the renamed `regulus/` package.
- Produces: a uv-resolvable project. After this task `uv sync` creates `.venv` + `uv.lock`. Dist name `gf-regulus`, wheel packages `regulus`. Dev tools available via `uv run` (pytest, ruff, mypy).

- [ ] **Step 1: Write `pyproject.toml`**

Create `python/regulus/pyproject.toml` with exactly:

```toml
[project]
name = "gf-regulus"
version = "0.1.0"
description = "Practical functional programming for Python — the pure functional core of goforge's Python wing. A hard fork of dbrattli/Expression."
readme = "README.md"
requires-python = ">=3.11"
license = { file = "LICENSE" }
authors = [{ name = "brain-fuel" }]
keywords = ["functional", "option", "result", "pipe", "monad", "fp"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
dependencies = ["typing-extensions>=4.6.0"]

[project.urls]
Homepage = "https://goforge.dev/python/regulus"
Repository = "https://github.com/brain-fuel/regulus"

[project.optional-dependencies]
pydantic = ["pydantic>=2.6.2"]

[dependency-groups]
dev = [
    "pytest>=8.3.3",
    "pytest-asyncio>=0.25.0",
    "hypothesis>=6.54.2",
    "ruff>=0.9.0",
    "mypy>=1.13.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["regulus"]

[tool.ruff]
line-length = 120
target-version = "py311"
extend-exclude = ["tests", "docs"]
lint.ignore = ["D100", "D101", "D102", "D103", "D105", "D107"]
lint.select = ["D", "E", "W", "F", "I", "T", "RUF", "TID", "UP"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
lines-after-imports = 2
known-third-party = ["pytest"]

[tool.mypy]
python_version = "3.11"
strict = true
files = ["regulus"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "strict"
```

- [ ] **Step 2: Write `.gitignore`**

Create `python/regulus/.gitignore` with exactly:

```gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
dist/
*.egg-info/
.coverage
htmlcov/
```

- [ ] **Step 3: Resolve and build the environment**

Run: `cd /home/brainfuel/matt/goforge.dev/python/regulus && uv sync --all-extras --dev`
Expected: uv creates `.venv` and writes `uv.lock`; ends with a "Installed N packages" / "Resolved N packages" summary and no error.

- [ ] **Step 4: Verify the package imports from the built env**

Run: `cd /home/brainfuel/matt/goforge.dev/python/regulus && uv run python -c "import regulus; from regulus.core import Option, Result, pipe; print(regulus.__version__)"`
Expected: prints `0.1.0`.

- [ ] **Step 5: Commit**

```bash
cd /home/brainfuel/matt/goforge.dev/python/regulus
git add pyproject.toml .gitignore uv.lock
git commit -m "build: uv + hatchling project config (gf-regulus, py3.11+)"
```

---

### Task 4: Green test suite under uv

**Files:**
- Test: `python/regulus/tests/` (already vendored + renamed)

**Interfaces:**
- Consumes: the uv env from Task 3.
- Produces: a passing test suite — the acceptance proof that the rename preserved behavior.

- [ ] **Step 1: Run the full suite**

Run: `cd /home/brainfuel/matt/goforge.dev/python/regulus && uv run pytest -q`
Expected: all tests pass (upstream has ~20 test modules; expect `N passed` with 0 failed, 0 errors). Skips are acceptable.

- [ ] **Step 2: If any test errors on a missed rename, fix it**

If a failure is an `ImportError`/`ModuleNotFoundError` mentioning `expression`, re-run the Task 2 Step 2 sed over the offending file, then re-run Step 1. (Expected: not needed — Task 2 Step 5 already proved zero stray refs.) If a failure is a genuine behavior difference, STOP and report — that contradicts "no API changes" and needs investigation, not a patch.

- [ ] **Step 3: Commit (only if Step 2 changed files)**

```bash
cd /home/brainfuel/matt/goforge.dev/python/regulus
git add -A
git commit -m "test: green pytest suite under regulus namespace"
```

If Step 2 made no changes, skip this commit.

---

### Task 5: License attribution, NOTICE, README

**Files:**
- Modify: `python/regulus/LICENSE` (append fork copyright line; retain upstream verbatim)
- Create: `python/regulus/NOTICE`
- Create: `python/regulus/README.md`

**Interfaces:**
- Consumes: nothing code-level.
- Produces: MIT compliance artifacts + the public README. `README.md` is referenced by `pyproject.toml` `readme = "README.md"`.

- [ ] **Step 1: Preserve upstream copyright, add fork line**

At the top of `python/regulus/LICENSE`, immediately under the existing `MIT License` heading and the original `Copyright (c) ...` line, add one line (do NOT remove or alter the original copyright):

```text
Copyright (c) 2026 brain-fuel (regulus fork)
```

- [ ] **Step 2: Write `NOTICE`**

Create `python/regulus/NOTICE` with exactly:

```text
regulus
Copyright (c) 2026 brain-fuel

This product is a hard fork of Expression
(https://github.com/dbrattli/Expression), Copyright (c) Dag Brattli and
contributors, licensed under the MIT License. The original MIT license text
is retained in the LICENSE file. regulus renames the `expression` import
namespace to `regulus` and is maintained independently of upstream.
```

- [ ] **Step 3: Write `README.md`**

Create `python/regulus/README.md` with exactly:

```markdown
# regulus

> The regulus is the button of pure, refined metal that settles at the bottom
> of the crucible, the slag skimmed off. `regulus` is the pure functional core
> of [goforge](https://goforge.dev)'s Python wing — type-safe Option, Result,
> pipe, effects, tagged unions, and immutable collections. No nulls, no naked
> exceptions; the dross stays out.

A hard fork of [dbrattli/Expression](https://github.com/dbrattli/Expression).

## Install

```bash
pip install gf-regulus      # import name is `regulus`
```

## Use

```python
from regulus.core import Option, Some, Nothing, pipe

result = pipe(
    Some(42),
    Option.map(lambda x: x + 1),
)
assert result == Some(43)
```

## Develop

```bash
uv sync --all-extras --dev
uv run pytest        # tests
uv run ruff check .  # lint
uv run mypy regulus  # types
```

## License

MIT. See `LICENSE` and `NOTICE`.
```

- [ ] **Step 4: Verify README is valid for the build backend**

Run: `cd /home/brainfuel/matt/goforge.dev/python/regulus && uv build 2>&1 | tail -3`
Expected: builds an sdist + wheel into `dist/` with no error (confirms `readme` + metadata resolve). It is fine to delete `dist/` after.

- [ ] **Step 5: Commit**

```bash
cd /home/brainfuel/matt/goforge.dev/python/regulus
rm -rf dist
git add LICENSE NOTICE README.md
git commit -m "docs: MIT NOTICE attribution + README (assayer voice)"
```

---

### Task 6: Lint + type gates

**Files:**
- Modify: `regulus/**/*.py` only if ruff reports auto-fixable lint errors
- Create: `python/regulus/docs/superpowers/notes/mypy-baseline.md` (only if mypy is not strict-clean)

**Interfaces:**
- Consumes: the uv env.
- Produces: a ruff-clean package and a recorded mypy posture. ruff is a required gate; mypy is advisory for v0.1 (upstream is tuned for pyright, so strict mypy may report findings — those are divergence-era work, not v0.1 blockers).

- [ ] **Step 1: Run ruff and auto-fix**

Run: `cd /home/brainfuel/matt/goforge.dev/python/regulus && uv run ruff check . && uv run ruff format --check .`
Expected: `All checks passed!` If ruff reports fixable issues, run `uv run ruff check --fix . && uv run ruff format .`, then re-run the check until clean. Do not edit code by hand for style — let ruff do it.

- [ ] **Step 2: Run mypy strict and record the result**

Run: `cd /home/brainfuel/matt/goforge.dev/python/regulus && uv run mypy regulus | tail -5`
Expected: either `Success: no issues found` OR a finite error count.

- If `Success`: no baseline file needed. Note in the commit that mypy strict is clean and the CI mypy step (Task 7) should be made required (`continue-on-error: false`).
- If errors: create `python/regulus/docs/superpowers/notes/mypy-baseline.md` recording the exact error count and the one-line summary `mypy --strict findings on the vendored Expression code; tracked for divergence, advisory in CI for v0.1.` Leave the code unchanged. The CI mypy step stays advisory.

- [ ] **Step 3: Commit**

```bash
cd /home/brainfuel/matt/goforge.dev/python/regulus
git add -A
git commit -m "chore: ruff clean; record mypy strict baseline"
```

---

### Task 7: GitHub Actions CI + tag

**Files:**
- Create: `python/regulus/.github/workflows/ci.yml`

**Interfaces:**
- Consumes: the whole project.
- Produces: CI running ruff + pytest (required) and mypy (advisory unless Task 6 found it clean) on Python 3.11 and 3.12, and the `v0.1.0` tag.

- [ ] **Step 1: Write the workflow**

Create `python/regulus/.github/workflows/ci.yml` with exactly:

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Sync
        run: uv sync --all-extras --dev
      - name: Lint
        run: uv run ruff check . && uv run ruff format --check .
      - name: Test
        run: uv run pytest -q
      - name: Types (advisory)
        run: uv run mypy regulus
        continue-on-error: true
```

(If Task 6 Step 2 found mypy strict-clean, set `continue-on-error: false` and drop "(advisory)" from the step name.)

- [ ] **Step 2: Validate the workflow YAML parses**

Run: `cd /home/brainfuel/matt/goforge.dev/python/regulus && uv run python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/ci.yml')); print('YAML_OK')"`
Expected: `YAML_OK`. (PyYAML is pulled in transitively; if missing, run `uv run --with pyyaml python -c "..."`.)

- [ ] **Step 3: Final full local gate before tagging**

Run: `cd /home/brainfuel/matt/goforge.dev/python/regulus && uv run ruff check . && uv run pytest -q && echo GATE_OK`
Expected: ends with `GATE_OK`.

- [ ] **Step 4: Commit and tag**

```bash
cd /home/brainfuel/matt/goforge.dev/python/regulus
git add .github/workflows/ci.yml
git commit -m "ci: GitHub Actions (uv, ruff + pytest required, mypy advisory) on py3.11/3.12"
git tag v0.1.0
```

- [ ] **Step 5: Report remaining owner-only steps**

These are NOT done by this plan — report them to the user:
- Create `github.com/brain-fuel/regulus` and push `main` + `v0.1.0`.
- Pursue PEP 541 transfer of the abandoned PyPI `regulus` (dead since 2019); interim dist name stays `gf-regulus`.
- PyPI publish is deferred until there are real consumers (per spec — out of v0.1 scope).

---

## Self-Review

**Spec coverage:**
- "Vendor + rename `expression/` → `regulus/`, fix imports" → Tasks 1, 2. ✓
- "uv pyproject, dist gf-regulus, py3.11+" → Task 3. ✓
- "Retain MIT LICENSE + NOTICE" → Task 5. ✓
- "ruff + mypy-strict configs" → Tasks 3 (config), 6 (run; mypy advisory rationale documented). ✓
- "Port full test suite; passes" → Task 4. ✓
- "GH Actions CI green on 3.11/3.12" → Task 7. ✓
- "README assayer voice" → Task 5. ✓
- "Tag v0.1.0" → Task 7. ✓
- "No API changes" → enforced by Task 4 Step 2 (genuine behavior diff = STOP). ✓
- Out-of-scope (PEP 541, PyPI publish, other tools, Polylith) → not implemented; PEP 541 + publish surfaced in Task 7 Step 5. ✓

**Placeholder scan:** No TBD/TODO; every code/config step shows full content; every command has expected output. The one conditional (mypy clean vs not) has both branches fully specified. ✓

**Type/name consistency:** Import package `regulus` and dist `gf-regulus` used consistently; `_version.py` `0.1.0` matches `pyproject` `version` matches the import-check in Task 3 Step 4; wheel `packages = ["regulus"]` matches the renamed dir. ✓

**Mypy-strict honesty:** v0.1 cannot guarantee strict-clean on code tuned upstream for pyright; the plan measures it, records a baseline, and keeps CI advisory rather than faking a green gate. Strict-clean is divergence-era work. ✓
