# SPDX-License-Identifier: MIT
# Copyright: 2024-2026 Paillat-dev

import requests

URL = "https://raw.githubusercontent.com/Discord-Datamining/Discord-Datamining/refs/heads/master/current.js"


def dowload() -> str:
    """Download the latest discord build from the datamining repository.

    Returns the content of the file as a string.
    """
    print("Downloading the latest discord build")
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    return response.text
