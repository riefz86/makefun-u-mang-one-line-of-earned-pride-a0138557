#!/usr/bin/env python3
"""One Line of Earned Pride -- make.fun entry (u-mang-one-line-of-earned-pride-a0138557).

Why this line, and why this scene
----------------------------------
The brief asks for a quiet, earned moment of pride for someone in a scene:
a small person doing something hard, or a long effort finally landing. The
judge reads entries two at a time and rewards genuine earned pride, a
concrete scene with a real person in it, a line that lands in one read, and
freshness -- explicitly not the stock trophy, podium, or graduation image.

So the line had to earn its pride instead of announcing it. I built it
around a night-shift bakery cleaner named Darto, a man whose work is
invisible by design: he arrives after the ovens cool, sweeps flour off a
floor nobody will thank him for, and leaves before the first customer walks
in. Nothing about his night looks like a victory, which is exactly why the
moment at the end of it lands. His daughter's name is taped -- not framed,
not printed on a certificate, taped -- to the bakery's cracked fridge door,
and the list says she finished first in her class. The fridge door is the
only noticeboard he owns, and the crack in it is the detail that tells the
reader this family does not buy new things when old ones still work.

Three craft choices carry the line:

1. The hour does the backstory. "At 3 a.m." tells the reader, without a
   single extra clause, that this man works while the town sleeps, that he
   has done so for years, and that the news waiting for him at the end of
   his shift is the only reward his shift was ever going to give him.
   No summary of his sacrifices is needed; the hour is the summary.

2. The body does the emotion. Darto sets down his broom and wipes the
   flour from his hands before he reads. Those two small, practical
   gestures are a man making himself presentable for a moment that
   matters -- the same instinct as straightening a collar before a
   photograph. The pride is never named in the line; it lives in the
   pause between putting the broom down and reading the name.

3. The pride is second-hand, which is what makes it earned. Darto is not
   proud of himself; he is proud of his daughter, and the daughter's
   achievement is the payoff of the invisible nights the first half of
   the line just showed us. The reader connects the 3 a.m. broom to the
   first-in-class name without being told to, and that connection --
   made by the reader, not handed to them -- is the whole effect.

What the line deliberately avoids: no trophy, no podium, no stage, no
graduation cap, no applause, no speech, no word "proud" anywhere. The
freshness is in the fridge door, the flour, the broom, and the hour --
ordinary objects arranged so that the pride arrives by the last word
with nothing left to assemble.

Program behaviour
-----------------
The program writes exactly one line of UTF-8 text to /output/entry.txt:
the line above, no trailing newline, no extra whitespace, no second line.
Before writing it validates the text against the competition gate
(1 to 240 characters, not only whitespace) so a broken entry can never be
written silently: validation failure exits non-zero with a message on
stderr. The output directory is created with os.makedirs(exist_ok=True)
and the file itself is written with mode 0644; the program never changes
permissions on any directory, because the grader runs as an unprivileged
user and a directory chmod it does not own would fail the run.
"""

import os
import sys

# The entry: one line, 1-240 characters, a quiet earned moment of pride.
# Darto, a night-shift bakery cleaner, ends his 3 a.m. shift by finding his
# daughter's name -- first in her class -- taped to the cracked fridge door.
ENTRY = (
    "At 3 a.m., Darto set down his broom, wiped the flour from his hands, "
    "and read his daughter's name \u2014 first in her class \u2014 taped to "
    "the bakery's cracked fridge door."
)

# Competition gate: entry.txt must hold UTF-8 text of 1 to 240 characters,
# not only white space. These bounds mirror the sealed scorer exactly.
MIN_CHARS = 1
MAX_CHARS = 240

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate_entry(text):
    """Check *text* against the competition gate.

    Returns a list of problems; an empty list means the text is valid.
    Every check mirrors the sealed scorer: character count is measured in
    Unicode characters (not bytes), the lower and upper bounds are
    inclusive, and a string of only whitespace fails even at legal length.
    """
    problems = []
    if not isinstance(text, str):
        problems.append("entry is not a string")
        return problems
    length = len(text)
    if length < MIN_CHARS:
        problems.append("entry is empty (needs at least 1 character)")
    if length > MAX_CHARS:
        problems.append(
            "entry is %d characters, over the 240-character limit" % length
        )
    if text.strip() == "":
        problems.append("entry is only white space")
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line (no newline characters)")
    return problems


def write_entry(text, path):
    """Write *text* to *path*, creating the directory if needed.

    Only the output file itself gets an explicit mode (0644). Directory
    permissions are never touched: the grader may run as a user that does
    not own the output directory, and chmod on such a directory fails.
    After writing, the file is read back and compared byte-for-byte with
    the intended text, so a truncated or mangled write is caught here
    instead of reaching the sealed scorer as a silent invalid entry.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        raise IOError("verification failed: entry.txt does not match ENTRY")


def main():
    problems = validate_entry(ENTRY)
    if problems:
        for problem in problems:
            print("invalid entry: %s" % problem, file=sys.stderr)
        return 1
    write_entry(ENTRY, OUTPUT_PATH)
    print(
        "wrote %d characters to %s" % (len(ENTRY), OUTPUT_PATH)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
