# Copyright (c) Paillat-dev
# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod


class ParseError(Exception, ABC):
    """Base class for all parsing errors."""


class BuildParser(ABC):
    """Base class for all build parsers."""

    FILE_NAME: str

    def __init__(self, discord_build: str) -> None:
        """Initialize the parser with the discord build.

        Args:
            discord_build (str): The content of the discord build to parse.

        """
        self.discord_build: str = discord_build

    @abstractmethod
    def __call__(self) -> tuple[bytes, str]:
        """Return a tuple of the parsed data we want to obtain and a hash for verifying whether the data has changed.

        Returns:
            Tuple[T, str]: A tuple containing the parsed data and a hash string.

        """
