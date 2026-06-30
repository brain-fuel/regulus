# regulus — design spec

> A hard fork of [dbrattli/Expression](https://github.com/dbrattli/Expression):
> the pure functional-programming foundation of goforge's Python wing.

- **Date:** 2026-06-30
- **Status:** approved, pre-implementation
- **Repo:** `github.com/brain-fuel/regulus`
- **Path:** `goforge.dev/python/regulus`
- **Import name:** `regulus`
- **Dist name:** `gf-regulus` (interim); PEP 541 transfer of abandoned PyPI `regulus` pursued in parallel
- **License:** MIT

## What regulus is

The **regulus** is the button of pure refined metal that settles at the bottom of
the crucible, separated from the slag. regulus the library is the Option / Result /
pipe / effects core of goforge's Python collection — the dross-free functional base
(no nulls, no naked exceptions) that every other Python tool in the suite is refined
from.

It is a hard fork of dbrattli/Expression, which brings F#/ML-style functional
programming to Python: `pipe`, `Option`, `Result`, `Try`, `AsyncResult`/`AsyncOption`,
`Seq`/`Block` immutable collections, `@tagged_union`, structural pattern matching,
parser combinators, computational-expression effects, and a mailbox processor.

### Naming

goforge's suite is named from metalworking *and assaying*. The Go side owns "forge"
(`goforge`). The Python side anchors on the assaying half. regulus = the pure metal
extracted, slag skimmed off — the metaphor *is* the one-line explanation of an
Option/Result library. The Python wing lives under `goforge.dev/python/<lib>`;
regulus is its first member.

## Why a hard fork (not a dependency)

Decision: **hard fork, diverge.** Vendor the source, rename to the `regulus`
namespace, own it outright, reshape the API to suite conventions over time, drop what
the suite does not want. No intent to track upstream. This trades upstream maintenance
for full control and coherence with the rest of goforge.

## License

regulus is **MIT** — matching upstream Expression. Rationale: a functional
foundation library wants broad adoption; MIT keeps attribution trivial and imposes no
copyleft friction on downstream goforge Python tools.

This is a deliberate exception to goforge's default software license (AGPL-3.0). The
exception is recorded here so the decision is auditable.

Obligations: retain Expression's original MIT `LICENSE` text, and add a `NOTICE`
crediting `dbrattli/Expression` as the fork origin.

## Local layout

A new `./python/` subtree in the goforge workspace mirrors the `goforge.dev/python/`
path:

```
goforge.dev/
  anvil/        # Go tool (existing)
  rune/         # Go tool (existing)
  ...
  python/
    regulus/    # this project (own brain-fuel repo)
```

Each Python lib is its own `brain-fuel` repo, same pattern as the Go tools. The
`python/` subtree leaves room for future Python libs in the collection.

## v0.1.0 scope — first green increment

Stand up a **working, renamed, attributed, tooled** fork. **No API changes in v0.1.**

1. Vendor Expression source; rename the `expression/` package → `regulus/`; fix all
   internal imports and references.
2. Replace `pyproject.toml`: **uv** build backend, dist name `gf-regulus`, Python
   **3.11+** floor.
3. Retain upstream **MIT `LICENSE`**; add `NOTICE` crediting dbrattli/Expression.
4. Add **ruff** (lint + format) and **mypy** (strict) configs.
5. Port the full upstream test suite; it must pass unmodified against the renamed
   package.
6. **GH Actions** CI: install via uv, run ruff + mypy + tests, green on 3.11 and 3.12.
7. `README.md` in the assayer voice (regulus = the pure refined button from the
   crucible).
8. Tag `v0.1.0`.

**Acceptance:** `import regulus` works; full ported test suite green; ruff clean; mypy
strict clean; CI green on 3.11 + 3.12; LICENSE + NOTICE present.

## Divergence — deferred, post-0.1

"Hard fork, diverge" proceeds *incrementally* after the green base, each as its own
small verified increment:

- Reshape naming to suite conventions.
- Decide keep/drop per module (e.g. mailbox processor, parser combinators).
- Align with goforge's purity / determinism worldview where it fits Python.

Explicitly **out of v0.1.**

## Out of scope

- Other Python tools in the collection (regulus is the foundation; the rest come
  later, each its own spec → plan → build cycle).
- PyPI publication — interim dist is `gf-regulus`; clean `regulus` waits on the PEP
  541 transfer. No publish required for v0.1.
- goforge brick / Polylith integration — Python is not Polylith; the Go worker-type
  model does not apply.

## Risks / open items

- **PyPI `regulus` is squatted** by an abandoned 2019 package (BSD-3, topology viz).
  PEP 541 transfer is plausible (7 years dead) but slow and not guaranteed; `gf-regulus`
  is the no-wait fallback. Same situation handled before for `wootz`.
- **Upstream drift** — by choosing a hard fork we forgo upstream bug fixes and new
  features; accepted as the cost of control.
