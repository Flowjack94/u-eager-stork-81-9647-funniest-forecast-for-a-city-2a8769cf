"""Funniest Forecast for a City That Isn't — one-line entry.

Builds the forecast line from named fragments, validates it against the
bounty gate (1-120 characters, one line, no control characters), and
writes it to $MAKEFUN_OUTPUT_DIR/entry.txt. Nothing is ever written into
the repository itself.
"""

import os


def build_forecast():
    """Assemble the one-line forecast from its named fragments."""
    city = "Tomorrow in Nowhereville"
    weather = "sunny, 24\u00b0C"
    mayor = "the mayor \u2014 who does not exist \u2014 opens the bridge"
    ticket = "ticket #4821"
    return f"{city}: {weather}, and {mayor} to {ticket}."


def guard_line(line):
    """Check the line against the bounty gate; raise if it fails."""
    if not 1 <= len(line) <= 120:
        raise ValueError(f"entry length {len(line)} outside 1-120")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        raise ValueError("entry contains control characters")
    return line


def publish(line):
    """Write the validated line to the grader output dir and verify it."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    with open(path, "rb") as fh:
        if fh.read() != data:
            raise IOError("entry.txt round-trip check failed")
    return path


def main():
    line = guard_line(build_forecast())
    publish(line)


if __name__ == "__main__":
    main()
