# awkwin's Codejam Library
This is my library collection used in codejams.

- `cjlib.baseN(num, base[, numerals])`: Convert `num` to base `base` with `numerals` as character representatives of values (default to 0-9a-z) [source](http://code.activestate.com/recipes/65212-convert-from-decimal-to-any-base-number/#c8)
- `cjlib.mathapi`: @neizod's mathapi. [Source and docs](https://github.com/neizod/mathapi)

# `input.py`
Input library. This library only works with only one input at a time. (i.e. `input.get` should be called only once)

- `input.get([default[, skip=True]])`: Read input from first command line argument or use `default`. Usually the first line is the lines count and will be automatically chopped. Disable this by setting `skip=False`.
- `input.line()`: Return next line from the input. (No line ending is included)
- `input.lines([cnt=2])`: Return next `cnt` lines from the input as an array.
- `input.block()`: Return next block in the same format as `input.lines` without the line number count. A block is defined as a line with a number showing how many lines are in this block. Example of a block:

~~~~~~~~~~
4
2 2 2
2 1 2
2 1 2
2 2 2
~~~~~~~~~~

Returns `["2 2 2", "2 1 2", "2 1 2", "2 2 2"]`.

- `input.neof()`: Return `True` if there is still more input. Usually used in a `while` loop.

# `runner.py`

Task multiprocessing.

Usage:

~~~~~~~~~~py
from cjlib.input import neof, line, get
from cjlib.runner import TaskRunner, DummyRunner

def is_odd(inp):
	return inp%2 == 1

r = TaskRunner(is_odd, DummyRunner)

get("""4
1
3
4
5
""")

while neof():
	r.add(int(line()))

r.run()
~~~~~~~~~~

- The second argument to `TaskRunner` is optional and use to specify multiprocessing backend. Defaults to `ThreadRunner`. Available modules are:
  - `DummyRunner`: Does not use multiprocessing. Easiest to debug.
  - `MPQRunner`: Use `multiprocessing.Pool`. Fastest but requires more memory.
  - `ThreadRunner`: Use `threading.Thread`. (Actually an `MPQRunner` with `multiprocessing.dummy.Pool` as thread pool)
- `MPQRunner` use 4 as hard-coded subprocess count. Supply `processCnt=8` to `TaskRunner` when using `MPQRunner` to use 8 processes and so on.
- The output will be returned in stdout after all backend has finished processing. Status messages are sent to Python's `logging` module with *info* level and usually be sent to stderr.
- To add case number to output, use `r.run(True)`. The output will be in Codejam format: `Case #n: out`
- Accessing `TaskRunner` in the processing function (in this case, `is_odd`) is not safe.