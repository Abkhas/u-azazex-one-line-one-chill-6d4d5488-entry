#!/usr/bin/env python3
"""One Line, One Chill — make.fun entry.

Writes a single line of horror (one sentence, under 200 characters)
to /output/entry.txt. Stdlib only, no network, no secrets.
"""

import os
import sys

LINE = "The insulation man pulled a child's shoe from my attic wall, then a second, then a third, all the same size, all still warm."

MAX_CHARS = 200


def resolve_output_dir():
    """MAKEFUN_OUTPUT_DIR wins, then /output, then a local out/ fallback."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def main():
    line = LINE
    if not line or not line.strip():
        print("error: entry line is empty", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(f"error: entry is {len(line)} chars, over the {MAX_CHARS} limit",
              file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: entry must be a single line", file=sys.stderr)
        return 1

    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")

    # Verify what was written: UTF-8, single line, 1..200 chars.
    with open(out_path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    body = text.rstrip("\n")
    assert 1 <= len(body) <= MAX_CHARS, "written entry out of range"
    assert "\n" not in body, "written entry is not a single line"
    print(f"wrote {out_path} ({len(body)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
