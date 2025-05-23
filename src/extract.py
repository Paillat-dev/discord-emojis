# Copyright (c) Paillat-dev
# SPDX-License-Identifier: MIT

import json
import re
from collections.abc import Mapping, Sequence
from typing import Any
from warnings import warn

import json5

type AnyDict = dict[Any, Any]  # pyright: ignore[reportExplicitAny]
type AnyList = list[Any]  # pyright: ignore[reportExplicitAny]
type AnyTuple = tuple[Any, ...]  # pyright: ignore[reportExplicitAny]

PATTERN = re.compile(r"""(?<=\(')(\{"emojis".*?\})(?='\))""")


class ExtractError(Exception):
    """Base class for all extract errors."""


class NotFoundError(ExtractError):
    """No matches found in the build."""


class MultipleFoundError(ExtractError):
    """Multiple matches found in the build."""


_SUR = re.compile(r"[\uD800-\uDFFF]")


def report_surrogates(node: AnyDict | AnyList | AnyTuple | str, path: str = "") -> None:
    r"""Recursively walk *node* (dict / list / tuple / str) and print the location and code-point of every UTF-16 surrogate half it encounters.

    >>> data = {"a": "OK", "b": ["\\uD83D", {"c": "x\\uDE00y"}]}
    >>> report_surrogates(data)
    b[0] : U+D83D
    b[1].c : U+DE00
    """  # noqa: E501
    if isinstance(node, str):
        for m in _SUR.finditer(node):
            cp = ord(m.group())
            warn(f"Surrogate found at {path or '<root>'} : U+{cp:04X}", SyntaxWarning, 2)
        return

    if isinstance(node, Mapping):
        for k, v in node.items():
            sub = f"{path}.{k}" if path else str(k)
            report_surrogates(v, sub)
        return

    if isinstance(node, Sequence) and not isinstance(node, (str, bytes, bytearray)):  # pyright: ignore[reportUnnecessaryIsInstance]
        for i, v in enumerate(node):
            report_surrogates(v, f"{path}[{i}]")


def extract_emojis_from_str(content: str) -> AnyDict:
    """Extract emojis from a string containing the discord build."""
    print("Searching for emojis...")
    matches: list[str] = PATTERN.findall(content)

    if len(matches) == 0:
        raise NotFoundError("No matches found")
    if len(matches) > 1:
        raise MultipleFoundError("Multiple matches found")

    match: str = matches[0]

    print("Found emojis!")
    print("Parsing json")

    # First load with json5 to handle \x escapes, then dump and reload with json to collapse
    # the surrogate pairs into a single code point. This is necessary because json5 doesn't
    # support surrogate pairs, and json doesn't support \x escapes.
    r = json.loads(json.dumps(json5.loads(match)))
    report_surrogates(r)

    return r
