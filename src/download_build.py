# Copyright (c) Paillat-dev
# SPDX-License-Identifier: MIT

import requests

URL = "https://raw.githubusercontent.com/Discord-Datamining/Discord-Datamining/refs/heads/master/current.js"


def dowload() -> str:
    print("Downloading the latest discord build")
    response = requests.get(URL)
    response.raise_for_status()
    return response.text
