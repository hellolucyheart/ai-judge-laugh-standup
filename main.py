#!/usr/bin/env python3
"""Standup discrimination — one line of office comedy.

Writes a single original joke about office life, one line and under
200 characters, to /output/entry.txt (falling back to entry.txt next
to this file when /output cannot be written, e.g. on a developer
machine).

The joke is fixed text: the entry is the writing itself, so the
program is deterministic — every run writes the same bytes.
"""

import os
import sys

PUNCHLINE = (
    "Our daily standup runs 45 minutes now, which is how I learned "
    "a standup is just a meeting that discriminates against chairs."
)

CHAR_LIMIT = 200


def tidy(text):
    """Collapse any stray whitespace to single spaces.

    The gate counts every character, so the line must be exactly the
    joke as written — no leading or trailing space, no double space.
    """
    return " ".join(text.split())


def check_line(line):
    """Refuse anything that would fail the sealed gate."""
    if not line.strip():
        return "joke is empty"
    if len(line) > CHAR_LIMIT:
        return f"joke is {len(line)} chars, over the {CHAR_LIMIT} limit"
    if "\n" in line or "\r" in line:
        return "joke must be a single line"
    return None


def write_entry(line):
    """Write the line to /output/entry.txt, or beside this file."""
    payload = line + "\n"
    primary_dir = "/output"
    try:
        os.makedirs(primary_dir, exist_ok=True)
        target = os.path.join(primary_dir, "entry.txt")
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(payload)
        return target
    except OSError:
        here = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(here, "entry.txt")
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(payload)
        return target


def main():
    line = tidy(PUNCHLINE)
    problem = check_line(line)
    if problem is not None:
        print(f"error: {problem}", file=sys.stderr)
        return 1

    target = write_entry(line)
    print(f"wrote {len(line)} chars to {target}")
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
