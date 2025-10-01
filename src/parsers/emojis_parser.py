# Copyright (c) Paillat-dev
# SPDX-License-Identifier: MIT

import hashlib
import json
import re
from typing import Literal, NotRequired, TypedDict, final, override

import json5

from .base import BuildParser, ParseError

PATTERN = re.compile(r"""(?<=\(')(\{"emojis".*?\})(?='\))""")


class EmojiParseError(ParseError):
    """Base class for all emoji parsing errors."""


class NotFoundError(EmojiParseError):
    """No matches found in the build."""


class MultipleFoundError(EmojiParseError):
    """Multiple matches found in the build."""


class EmojiData(TypedDict):
    """Structure of an emoji's data."""

    names: list[str]
    surrogates: str
    unicodeVersion: float
    spriteIndex: int
    hasMultiDiversityParent: NotRequired[bool]


class EmojisData(TypedDict):
    """Structure of the extracted emojis data."""

    emojis: list[EmojiData]
    emojisByCategory: dict[str, list[int]]
    nameToEmoji: dict[str, int]
    surrogateToEmoji: dict[str, int]
    numDiversitySprites: int
    numNonDiversitySprites: int


_SUR = re.compile(r"[\uD800-\uDFFF]")


@final
class EmojisParser(BuildParser):
    """Parser for extracting emojis from the discord build."""

    FILE_NAME: Literal["emojis.json"] = "emojis.json"  # pyright: ignore[reportIncompatibleVariableOverride]

    @override
    def __call__(self) -> tuple[bytes, str]:
        """Extract emojis from the discord build and return them as a JSON dump and a hash.

        Returns:
            Tuple[bytes, str]: A tuple containing the JSON dump of the emojis and a SHA-256 hash of the dump.

        """
        extracted = self.extract_emojis_from_str(self.discord_build)
        new_dump = json.dumps(extracted, indent=4, ensure_ascii=False).encode("utf-8")
        new_hash = hashlib.sha256(string=new_dump).hexdigest()
        return new_dump, new_hash

    @staticmethod
    def extract_emojis_from_str(content: str) -> EmojisData:
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
        r: EmojisData = json.loads(json.dumps(json5.loads(match)))

        return r
