# Copyright (c) Paillat-dev
# SPDX-License-Identifier: MIT

import os
import pathlib
import hashlib
import json

import sys
from typing import Any

from extract import extract_emojis_from_str
from download_build import dowload


def main() -> None:
    build_path = pathlib.Path(os.getcwd()) / "build"
    build_path.mkdir(exist_ok=True)

    out_path = build_path / "emojis.json"
    hash_path = build_path / "hash.txt"

    if not out_path.exists():
        out_path.touch()

    if hash_path.exists():
        with hash_path.open("r", encoding="utf-8") as hash_file:
            current_hash = hash_file.read()
    else:
        current_hash = ""

    new: dict[Any, Any] = extract_emojis_from_str(dowload())  # pyright: ignore[reportExplicitAny]
    new_dump = json.dumps(new, indent=4, ensure_ascii=False).encode("utf-8")
    new_hash = hashlib.sha256(string=new_dump).hexdigest()

    if current_hash == new_hash:
        print("No changes")
        sys.exit(3)  # No changes

    with out_path.open("wb") as out_file:
        out_file.write(new_dump)

    with hash_path.open("w", encoding="utf-8") as hash_file:
        hash_file.write(new_hash)

    print("Updated emojis.json")


if __name__ == "__main__":
    main()
