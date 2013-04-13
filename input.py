import sys

inp = None

def get(default="", skip=True):
	global inp
	if len(sys.argv) > 1:
		inp = map(lambda x: x.strip(), open(sys.argv[1]).readlines())
	else:
		inp = default.split("\n")
	if skip:
		inp = inp[1:]
	return inp

def line():
	global inp
	return inp.pop(0)

def lines(cnt=2):
	global inp
	out = []
	for x in xrange(cnt):
		out.append(line())
	return out

def block():
	"""Read a block. Block start with a number telling how much is in that block.
	The block length is truncated"""
	out = []
	for x in range(int(line())):
		out.append(line())
	return out

def neof():
	return len(inp) > 0