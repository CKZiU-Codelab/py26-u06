#!/usr/bin/env python3
"""Self-check for the project "Prime Spiral" (u06).

Run it in the project directory:

    python3 check.py

The script reads only the files your program produced. It never runs
your program, so generate the files first, then check them. Each
[fail] line names one requirement; fix it and run the script again.
"""

import csv
import html as html_lib
import os
import re
import sys


class Fail(Exception):
    pass


CHECKS = []
WARNINGS = []


def check(name):
    def register(function):
        CHECKS.append((name, function))
        return function
    return register


def warn(message):
    WARNINGS.append(message)


def read_text(path):
    if not os.path.exists(path):
        raise Fail("%s is missing" % path)
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def read_csv(path):
    if not os.path.exists(path):
        raise Fail("%s is missing" % path)
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise Fail("%s is empty" % path)
    return rows


def require_files(*names):
    missing = [name for name in names if not os.path.exists(name)]
    if missing:
        raise Fail("missing: %s" % ", ".join(missing))


def require_notes(*headings):
    text = read_text("notes.md")
    missing = [heading for heading in headings if heading not in text]
    if missing:
        raise Fail("notes.md has no section: %s" % " | ".join(missing))


def read_pnm(path):
    text = read_text(path)
    lines = [line.split("#")[0] for line in text.splitlines()]
    tokens = " ".join(lines).split()
    if not tokens:
        raise Fail("%s is empty" % path)
    magic = tokens[0]
    if magic not in ("P1", "P2", "P3"):
        raise Fail("%s starts with %r; use the text formats P1, P2 or P3" % (path, magic))
    try:
        width = int(tokens[1])
        height = int(tokens[2])
    except (IndexError, ValueError):
        raise Fail("%s: the width and the height are missing from the header" % path)
    index = 3
    maxval = 1
    if magic in ("P2", "P3"):
        try:
            maxval = int(tokens[3])
        except (IndexError, ValueError):
            raise Fail("%s: the maximum value is missing from the header" % path)
        index = 4
    channels = 3 if magic == "P3" else 1
    needed = width * height * channels
    values = tokens[index:]
    if len(values) != needed:
        raise Fail("%s: the header says %dx%d, which needs %d values, but the file has %d"
                   % (path, width, height, needed, len(values)))
    try:
        numbers = [int(value) for value in values]
    except ValueError:
        raise Fail("%s contains a value that is not an integer" % path)
    for number in numbers:
        if number < 0 or number > maxval:
            raise Fail("%s has the value %d, outside 0..%d" % (path, number, maxval))
    return {"magic": magic, "width": width, "height": height,
            "maxval": maxval, "values": numbers, "path": path}


def find_frames(minimum=8):
    if not os.path.isdir("frames"):
        raise Fail("the frames/ directory is missing")
    names = sorted(name for name in os.listdir("frames") if name.endswith(".pgm"))
    if not names:
        raise Fail("frames/ has no .pgm files")
    bad = [name for name in names if not re.match(r"^frame_\d\d\.pgm$", name)]
    if bad:
        raise Fail("these names do not use two digits: %s" % ", ".join(bad[:3]))
    if len(names) < minimum:
        raise Fail("only %d frames; the animation needs at least %d" % (len(names), minimum))
    return ["frames/" + name for name in names]


def numbers_in(text):
    return [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", text)]


def require_gif(path):
    if not os.path.exists(path):
        raise Fail("%s is missing; build it with the convert command from the brief" % path)
    with open(path, "rb") as handle:
        head = handle.read(6)
    if not head.startswith(b"GIF8"):
        raise Fail("%s does not start with GIF8; is it really a GIF?" % path)


def scan_sources(forbidden):
    for name in sorted(os.listdir(".")):
        if not name.endswith(".py") or name == "check.py":
            continue
        with open(name, encoding="utf-8") as handle:
            for number, line in enumerate(handle, start=1):
                code = line.split("#")[0]
                for token in forbidden:
                    if token in code:
                        warn("%s:%d uses %s; the brief asks for a different tool."
                             % (name, number, token))


def main():
    print("")
    print("Checking the project in %s" % os.getcwd())
    print("")
    passed = 0
    failed = 0
    for name, function in CHECKS:
        try:
            function()
        except Fail as error:
            failed += 1
            print("[fail] %s" % name)
            print("       %s" % error)
        except Exception as error:
            failed += 1
            print("[fail] %s" % name)
            print("       the check itself stopped: %s: %s" % (type(error).__name__, error))
        else:
            passed += 1
            print("[ok]   %s" % name)
    print("")
    for message in WARNINGS:
        print("[warn] %s" % message)
    if WARNINGS:
        print("")
    print("%d passed, %d failed" % (passed, failed))
    if failed:
        print("NOT READY YET - fix the [fail] lines above and run the script again.")
        return 1
    print("PROJECT READY - every automatic check passed. Show the program and notes.md.")
    return 0



def spiral_image():
    image = read_pnm("spiral.pgm")
    if image["magic"] != "P2":
        raise Fail("spiral.pgm is %s; the picture uses the PGM format P2" % image["magic"])
    if image["width"] != image["height"]:
        raise Fail("spiral.pgm is %dx%d; the spiral is square"
                   % (image["width"], image["height"]))
    side = image["width"]
    if side % 2 == 0 or side < 9 or side > 101:
        raise Fail("side %d; n must be odd, between 9 and 101" % side)
    return image


def rings_data():
    rows = read_csv("rings.csv")
    header = [cell.strip().lower() for cell in rows[0]]
    if header != ["ring", "numbers", "primes", "share"]:
        raise Fail("rings.csv header is %s; expected ring,numbers,primes,share"
                   % ",".join(header))
    data = []
    for number, row in enumerate(rows[1:], start=2):
        if len(row) != 4:
            raise Fail("line %d of rings.csv has %d cells, four expected" % (number, len(row)))
        try:
            ring = int(row[0])
            numbers = int(row[1])
            primes = int(row[2])
            share = float(row[3])
        except ValueError:
            raise Fail("line %d of rings.csv is not numeric" % number)
        if numbers <= 0:
            raise Fail("line %d of rings.csv has %d numbers" % (number, numbers))
        if primes < 0 or primes > numbers:
            raise Fail("line %d of rings.csv has %d primes out of %d numbers"
                       % (number, primes, numbers))
        expected = 100.0 * primes / numbers
        if abs(share - expected) > 0.2:
            raise Fail("line %d says %.1f%%, but %d of %d is %.1f%%"
                       % (number, share, primes, numbers, expected))
        data.append((ring, numbers, primes))
    return data


@check("the files named in the brief exist")
def files():
    require_files("primes.py", "spiral.py", "spiral.pgm", "rings.csv",
                  "frames.csv", "spiral.gif", "notes.md")


@check("spiral.pgm is a square picture with two values")
def spiral():
    image = spiral_image()
    values = set(image["values"])
    if len(values) > 2:
        raise Fail("the picture has %d different values; a spiral of primes needs two"
                   % len(values))
    if not values <= {0, image["maxval"]}:
        raise Fail("the two values are %s; use 0 and the maximum value" % sorted(values))


@check("rings.csv has the four columns and the rings add up to the grid")
def rings():
    image = spiral_image()
    side = image["width"]
    data = rings_data()
    total_numbers = 0
    for ring, numbers, primes in data:
        total_numbers += numbers
    if total_numbers != side * side:
        raise Fail("the numbers in rings.csv add up to %d, but the grid has %d cells"
                   % (total_numbers, side * side))
    expected_rings = (side + 1) // 2
    if len(data) != expected_rings:
        raise Fail("rings.csv has %d rings; a %dx%d spiral has %d"
                   % (len(data), side, side, expected_rings))


@check("the black pixels are exactly the primes counted in rings.csv")
def black_pixels():
    image = spiral_image()
    black = 0
    for value in image["values"]:
        if value == 0:
            black += 1
    primes = 0
    for ring, numbers, count in rings_data():
        primes += count
    if black != primes:
        raise Fail("the picture has %d black pixels and rings.csv counts %d primes. "
                   "In a PGM file the value 0 is black." % (black, primes))


@check("frames/ holds at least eight square frames that grow")
def frames():
    paths = find_frames()
    sides = []
    for path in paths:
        image = read_pnm(path)
        if image["magic"] != "P2":
            raise Fail("%s is %s; the frames use the PGM format P2" % (path, image["magic"]))
        if image["width"] != image["height"]:
            raise Fail("%s is %dx%d; every frame is square"
                       % (path, image["width"], image["height"]))
        sides.append(image["width"])
    for first, second in zip(sides, sides[1:]):
        if second < first:
            raise Fail("the frames do not grow: %s" % sides)


@check("frames.csv has one row per frame")
def frame_rows():
    rows = read_csv("frames.csv")
    count = len(find_frames())
    if len(rows) - 1 != count:
        raise Fail("frames.csv has %d data rows and frames/ has %d frames"
                   % (len(rows) - 1, count))


@check("spiral.gif is a GIF file")
def gif():
    require_gif("spiral.gif")


@check("notes.md has both research notes and the picture note")
def notes():
    require_notes("## The New Thing – a grid of cells",
                  "## The New Thing – testing for a prime",
                  "## Milestone 4 – what the picture shows")


scan_sources(["dict"])

if __name__ == "__main__":
    sys.exit(main())
