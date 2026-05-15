#!/usr/bin/env python3
"""Bold configured speaker names when they appear at the start of a line as 'Name:'.

Example:
  python3 scripts/WSJ_bold_leading_speakers.py test2.md \
    --speaker "Imani Mosise" \
    --speaker "David Sanger" \
    --output test2.bold.md
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Bold configured speaker names when a line starts with "
            "'Speaker Name:'. Only exact leading speaker matches are changed."
        )
    )
    parser.add_argument("input", type=Path, help="Path to the source Markdown file.")
    parser.add_argument(
        "--speaker",
        action="append",
        dest="speakers",
        required=True,
        help="Speaker name to bold when it appears at the start of a line followed by a colon.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output path. If omitted, the input file is overwritten.",
    )
    parser.add_argument(
        "--ignore-case",
        action="store_true",
        help="Match configured speaker names case-insensitively.",
    )
    return parser.parse_args()


def normalize(value: str, ignore_case: bool) -> str:
    return value.casefold() if ignore_case else value


def bold_leading_speakers(content: str, speakers: list[str], ignore_case: bool) -> str:
    speaker_map = {normalize(speaker, ignore_case): speaker for speaker in speakers}
    output_lines: list[str] = []

    for line in content.splitlines(keepends=True):
        line_ending = ""
        if line.endswith("\r\n"):
            line_ending = "\r\n"
            core = line[:-2]
        elif line.endswith("\n"):
            line_ending = "\n"
            core = line[:-1]
        else:
            core = line

        matched = False
        for _, original_speaker in speaker_map.items():
            prefix = f"{original_speaker}:"
            core_prefix = core[: len(prefix)]

            if normalize(core_prefix, ignore_case) != normalize(prefix, ignore_case):
                continue

            rest = core[len(prefix) :]
            output_lines.append(f"**{core[:len(prefix)]}**{rest}{line_ending}")
            matched = True
            break

        if not matched:
            output_lines.append(line)

    return "".join(output_lines)


def main() -> None:
    args = parse_args()
    input_path = args.input
    output_path = args.output or input_path

    content = input_path.read_text(encoding="utf-8")
    updated = bold_leading_speakers(content, args.speakers, args.ignore_case)
    output_path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
