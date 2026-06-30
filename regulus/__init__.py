"""regulus — practical functional programming for Python.

regulus is the pure, dross-free functional core of goforge's Python wing:
type-safe Option, Result, pipe, effects, tagged unions, and immutable
collections. A hard fork of dbrattli/Expression.

GitHub: https://github.com/brain-fuel/regulus
"""

from . import collections, core, effect
from ._version import __version__
from .core import (
    AsyncReplyChannel,
    Builder,
    EffectError,
    Error,
    Failure,
    MailboxProcessor,
    Nothing,
    Ok,
    Option,
    Result,
    Some,
    Success,
    TailCall,
    TailCallResult,
    Try,
    case,
    compose,
    curry,
    curry_flip,
    default_arg,
    downcast,
    failwith,
    flip,
    fst,
    identity,
    is_error,
    is_none,
    is_ok,
    is_some,
    option,
    pipe,
    pipe2,
    pipe3,
    result,
    snd,
    tag,
    tagged_union,
    tailrec,
    tailrec_async,
    try_downcast,
    upcast,
)


curry_flipped = curry_flip
"""Deprecated.

Will be removed in next major version. Use curry_flip instead.
"""

__all__ = [
    "AsyncReplyChannel",
    "Builder",
    "EffectError",
    "Error",
    "Failure",
    "MailboxProcessor",
    "Nothing",
    "Ok",
    "Option",
    "Result",
    "Some",
    "Success",
    "TailCall",
    "TailCallResult",
    "Try",
    "__version__",
    "case",
    "collections",
    "compose",
    "core",
    "curry",
    "curry_flip",
    "curry_flipped",
    "default_arg",
    "downcast",
    "effect",
    "failwith",
    "flip",
    "fst",
    "identity",
    "is_error",
    "is_none",
    "is_ok",
    "is_some",
    "option",
    "pipe",
    "pipe2",
    "pipe3",
    "result",
    "snd",
    "tag",
    "tagged_union",
    "tailrec",
    "tailrec_async",
    "try_downcast",
    "upcast",
]
