# SPDX-License-Identifier: MIT
# Copyright: 2024-2026 Paillat-dev

from typing import TYPE_CHECKING

from .emojis_parser import EmojisParser

if TYPE_CHECKING:
    from .base import BuildParser

PARSERS: list[type[BuildParser]] = [EmojisParser]

__all__ = ("PARSERS", "EmojisParser")
