# regulus

> The regulus is the button of pure, refined metal that settles at the bottom
> of the crucible, the slag skimmed off. `regulus` is the pure functional core
> of [goforge](https://goforge.dev)'s Python wing - type-safe Option, Result,
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
