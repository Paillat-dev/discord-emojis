# Copyright (c) Paillat-dev
# SPDX-License-Identifier: MIT

from .base import BuildParser
from .emojis_parser import EmojisParser

PARSERS: list[type[BuildParser]] = [EmojisParser]

__all__ = ("PARSERS", "EmojisParser")
