# Project – Prime Spiral

**Individual Project Brief – Week 6 · u06**

Start: Monday, 16 November 2026. Show the working program on Monday, 23 November 2026.

## The Idea

You build a machine that draws primes as a picture. The program writes the numbers from 1 to N² into a square spiral — one in the middle, two to the right, three above, and so on around — marks every prime in black and every other number in white, and saves the grid as a PGM file. Then it counts the primes ring by ring, writes the counts to a CSV file and produces frames of a growing spiral that `convert` joins into a GIF.

This is the Ulam spiral, and it is one of the few places where arithmetic becomes visible. Nobody expects a pattern; a pattern appears anyway, in diagonals. Your program does not explain the pattern — it shows it, and then measures it.

## Why This Project Is Yours

You like mathematics, chess, origami and geography, and you are thinking about data science and cognitive science. All of those are about structure that appears when you arrange things in the right order. A spiral of numbers is the cheapest experiment of that kind: a small program, a big picture, and a real question at the end — why do the primes line up? You also recognize flags, which means you already read images as information rather than as decoration.

## What You Already Have

- Lists, tuples, slices, `for` and `while` loops, and nested loops from the PBM week.
- Conditions and logical operators, `%` for remainders, `//` for whole division.
- `%s`, `%d` and `%.1f` formatting, the `csv` module, and the PGM format.

## The New Thing

A spiral is a walk, and a walk needs a rule. Find out how to:

1. Store a two-dimensional grid as a list of lists, and how to address one cell with two indices.
2. Fill such a grid with nested loops and print it as text, one row per line.
3. Stop a loop early with `break`, and what happens to the `else` that belongs to a `for` loop.
4. Test whether a number is prime with trial division, and which largest divisor is enough to test.
5. Explain why testing every number up to `n - 1` is slower than testing up to the square root, and what `math.isqrt()` returns.
6. Change direction in a `while` loop without writing four separate loops.

**Write it down:** Create `notes.md` with `## The New Thing – a grid of cells`. Draw a three-by-three grid on paper, number the cells with two indices, and write two sentences about the order of the indices. Add `## The New Thing – testing for a prime` with the rule you use, one number that your rule handles correctly and one that it gets wrong if you are careless, and the line where `break` saves work.

## The Plan

### Milestone 1 – Is it prime?

Create `primes.py`.

1. Write the test for one number with a loop and a counter of divisors.
2. Print the primes from `2` to `50`, comma-separated, and count them.
3. Print the same list with `break` in the loop and compare the two versions.
4. Time both versions for `99991` — or count the loop turns with a counter if you do not want to use a timer — and write down the difference.

At the end of this step the program prints the primes up to fifty and you can say why the second version is faster.

### Milestone 2 – A grid you can see

1. Build an `n` by `n` grid of zeros with nested loops, where `n` comes from `input()`.
2. Print it as text with `.` for zero and `#` for one.
3. Set a few cells by hand with two indices and print the grid again.
4. Print the value of the cell in the middle, and the cell in the last row and last column.

At the end of this step you can fill any cell of the grid from its row and column number.

### Milestone 3 – The walk

1. Start in the middle of the grid at number `1`.
2. Move right, then up, then left, then down, and make each straight run two steps longer than the run before it.
3. Stop when the grid is full, and write the current number into the cell you are standing on.
4. Print the finished grid as text with the numbers modulo ten, or with the primes marked.

At the end of this step the text preview shows a spiral, and the number in the centre is `1`.

### Milestone 4 – The picture

1. Mark a cell black when its number is prime and white when it is not.
2. Write `spiral.pgm` with a `P2` header, one row of numbers per line.
3. Open the file and find the diagonals.
4. Write one sentence in `notes.md` about what you see, and one sentence about what you expected.

At the end of this step the picture is a valid PGM file and the diagonals are visible in a viewer.

### Milestone 5 – Measure it

1. Group the cells by ring: the centre is ring `0`, the next square ring is `1`, and so on. The largest number in ring `k` is `(2k + 1)²`.
2. Count the primes in every ring.
3. Write `rings.csv` with `ring,numbers,primes,share` and the share formatted with `%.1f`.
4. Print the share of primes for the whole grid, and compare it with the count of primes below `n²` from your own test.

### Milestone 6 – Make it move

1. Generate eight frames for growing `n`, from `21` to `101`, into `frames/frame_01.pgm` and so on.
2. Number the files with `%02d` and build `spiral.gif` with `convert -delay 40 -loop 0 frames/frame_*.pgm spiral.gif`.
3. Check that the spiral grows in the same direction in every frame, without jumping.
4. Write the frame sizes to `frames.csv` so the GIF can be traced back to the data.

## Example

```text
n (odd number, 9-101): 21

Text preview
.........#...........
.#.......#...........
..#..................
...

Prime share: 19.3% of 441 numbers
Ring 0: 0 of 1 numbers (0.0%)
Ring 1: 4 of 8 numbers (50.0%)
Ring 2: 5 of 16 numbers (31.3%)
...

Saved spiral.pgm (21x21)
Saved rings.csv (11 rows)
Saved frames.csv (8 rows)

$ convert -delay 40 -loop 0 frames/frame_*.pgm spiral.gif
Saved spiral.gif
```

The percentages are an example. Your grid and your counts decide your numbers.

## Requirements

- One program, `spiral.py`, started from the terminal with `python3 spiral.py`.
- The grid is a list of lists, and the walk is one `while` loop that changes direction, not four loops in sequence.
- The prime test uses `break`, and the bound of the search is explained in `notes.md`.
- `n` is validated: odd, at least `9`, at most `101`, and the grid is sized from that value.
- `spiral.pgm` has a correct header and exactly `n` rows of `n` values.
- `rings.csv` and `frames.csv` are written with the `csv` module and can be re-read.
- No drawing library: the picture is written by your own `write()` calls.

## Files

```text
prime_spiral/
├── primes.py
├── spiral.py
├── spiral.pgm
├── rings.csv
├── frames/
│   ├── frame_01.pgm
│   └── ...
├── frames.csv
├── spiral.gif
├── notes.md
└── check.py
```

Commit the whole directory to your repository and push it before the Monday session. A directory that exists only on your laptop cannot be checked.

Run `python3 check.py` in the project directory before you commit. It reads the files your program produced, not your code, and prints one line per requirement.


## How It Will Be Checked

- The spiral contains every number from `1` to `n²` exactly once.
- The number in the middle of the grid is `1`, and the number in a chosen corner matches `(2k + 1)²`.
- The prime test agrees with a hand-checked list for the numbers below one hundred.
- The ring counts add up to the number of cells in the grid.
- The GIF frames are all valid PGM files and the animation grows without shifting.
- You can explain the direction rule of the walk in three sentences, without the code.

**Hint:** Write the walk on paper first, cell by cell, for `n = 5`. Mark the run lengths — `1, 1, 2, 2, 3, 3, 4, 4` — and you have the rule. In code, keep the direction as two numbers, `dr` and `dc`, and change them at the end of every run.

**Additional challenge:** Draw the same spiral twice, once for the primes and once for the numbers that are not prime, and compare the two pictures. Then look for a second property to mark instead of primality — a perfect square, a number whose digits sum to a prime, a Fibonacci number — and write `rings.csv` for that property as well. Say in `notes.md` which of the two pictures shows more structure.

## Suggested Learning Resources

- [The `math` module – `isqrt`, `sqrt` and other functions](https://docs.python.org/3/library/math.html)
- [More on lists – nested lists and indexing](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
- [`break`, `continue` and the `else` clause on loops](https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops)
- [Ulam spiral – background and the diagonal patterns](https://en.wikipedia.org/wiki/Ulam_spiral)
- [Netpbm – description of the PGM format](https://netpbm.sourceforge.net/doc/pgm.html)

**Final goal:** By the end of this project, you should have a program that walks a two-dimensional grid, tests numbers for primality with an early exit, draws the result as a PGM picture, measures it ring by ring and animates it — using nested loops, conditions, lists and file handling from the first five weeks, and one new idea of your own research.
