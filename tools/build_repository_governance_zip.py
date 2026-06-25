#!/usr/bin/env python3
"""Build the runtime repository-governance extension zip."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


RUNTIME_ENTRIES = [
    Path("extension.yml"),
    Path("commands/speckit.repository-governance.generate.md"),
    Path("scripts/generate_repository_governance.py"),
    Path("templates/repository-governance-template.md"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="dist/repository-governance.zip", help="Zip file path to create.")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for file_path in RUNTIME_ENTRIES:
            if not file_path.is_file():
                raise SystemExit(f"Missing runtime asset: {file_path.as_posix()}")
            info = ZipInfo(file_path.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, file_path.read_bytes())

    print(output.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
