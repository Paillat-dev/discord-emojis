# Copyright (c) Paillat-dev
# SPDX-License-Identifier: MIT

import pathlib
import sys

from download_build import dowload
from parsers import PARSERS


def main() -> None:
    """Download the latest discord build and extract emojis."""
    build_path = pathlib.Path.cwd() / "build"
    build_path.mkdir(exist_ok=True)

    changes: bool = False

    build_download: str = dowload()
    for parser_cls in PARSERS:
        parser = parser_cls(build_download)
        out_path = build_path / parser.FILE_NAME
        hash_path = build_path / f".{parser.FILE_NAME}.hash"

        if not out_path.exists():
            out_path.touch()

        if hash_path.exists():
            with hash_path.open("r", encoding="utf-8") as hash_file:
                current_hash = hash_file.read()
        else:
            current_hash = ""

        new_dump: bytes
        new_hash: str
        new_dump, new_hash = parser()

        if current_hash == new_hash:
            print(f"No changes for {parser.FILE_NAME}")
            continue

        with out_path.open("wb") as out_file:
            out_file.write(new_dump)

        with hash_path.open("w", encoding="utf-8") as hash_file:
            hash_file.write(new_hash)

        changes = True
        print("Updated emojis.json")

    if not changes:
        sys.exit(3)  # No changes


if __name__ == "__main__":
    main()
