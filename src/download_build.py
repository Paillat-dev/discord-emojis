# SPDX-License-Identifier: MIT
# Copyright: 2024-2026 Paillat-dev

import os
import re
from typing import Final

import requests

COMMITS_URL: Final = "https://api.github.com/repos/Discord-Datamining/Discord-Datamining/commits"
ASSET_BASE_URL: Final = "https://discord.com/assets"
ASSET_PATTERN: Final = re.compile(r"\bvnd-emoji\.[0-9a-f]{16}\.js\b")


class DownloadError(RuntimeError):
    """The current Discord emoji bundle could not be located or downloaded."""


def _github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _find_asset_filename() -> str:
    """Find the current emoji vendor filename via Discord-Datamining's commit history.

    current.js no longer inlines the emoji data directly; it's split into a
    separate vnd-emoji.<hash>.js chunk that's only referenced in the commit
    messages of the Discord-Datamining repo.
    """
    response = requests.get(
        COMMITS_URL,
        params={"path": "current.js", "per_page": 5},
        headers=_github_headers(),
        timeout=30,
    )
    response.raise_for_status()

    for item in response.json():
        match = ASSET_PATTERN.search(item["commit"]["message"])
        if match is not None:
            return match.group(0)

    raise DownloadError("No vnd-emoji asset was listed in the latest Discord-Datamining commits")


def dowload() -> str:
    """Download the current Discord emoji vendor bundle.

    Returns the content of the file as a string.
    """
    filename = _find_asset_filename()
    print(f"Downloading Discord emoji bundle: {filename}")
    response = requests.get(f"{ASSET_BASE_URL}/{filename}", timeout=60)
    response.raise_for_status()
    return response.text
