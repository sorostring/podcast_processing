#!/usr/bin/env python3
"""Promote exact standalone lines in a Markdown file to level-2 headings.

Example:
  python3 scripts/bold_standalone_lines.py test.md \
    --term "rachel abrams" \
    --term "david sanger" \
    --term "[advertisements]" \
    --output test.heading.md
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert standalone lines to Markdown level-2 headings when the "
            "full line matches one of the provided target terms."
        )
    )
    parser.add_argument("input", type=Path, help="Path to the source Markdown file.")
    parser.add_argument(
        "--term",
        action="append",
        dest="terms",
        required=True,
        help="A standalone line to convert into a level-2 heading. Repeat for multiple values.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output path. If omitted, the input file is overwritten.",
    )
    parser.add_argument(
        "--ignore-case",
        action="store_true",
        help="Match standalone lines case-insensitively.",
    )
    return parser.parse_args()


def normalize(value: str, ignore_case: bool) -> str:
    stripped = value.strip()
    return stripped.casefold() if ignore_case else stripped

def is_already_heading(line: str) -> bool:
    return line.lstrip().startswith("## ")


def heading_matching_lines(content: str, terms: list[str], ignore_case: bool) -> str:
    normalized_terms = {normalize(term, ignore_case) for term in terms}
    output_lines: list[str] = []

    for line in content.splitlines(keepends=True):
        stripped = line.strip()

        if not stripped or is_already_heading(line):
            output_lines.append(line)
            continue

        if normalize(line, ignore_case) not in normalized_terms:
            output_lines.append(line)
            continue

        line_ending = ""
        if line.endswith("\r\n"):
            line_ending = "\r\n"
        elif line.endswith("\n"):
            line_ending = "\n"

        core = line.strip()
        output_lines.append(f"## {core}{line_ending}")

    return "".join(output_lines)


def main() -> None:
    args = parse_args()
    input_path = args.input
    output_path = args.output or input_path

    content = input_path.read_text(encoding="utf-8")
    updated = heading_matching_lines(content, args.terms, args.ignore_case)
    output_path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
