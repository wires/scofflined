import json, pygments

def pp(obj):
	"""Pretty print an object"""

	from pygments import highlight
	from pygments.lexers import JsonLexer
	from pygments.formatters import TerminalFormatter

	s = json.dumps(obj, indent=2, sort_keys=True)

	print(highlight(s, JsonLexer(), TerminalFormatter()))

def select(D,keys):
	return dict((k,v) for k,v in D.items() if k in set(keys))

def proj(D,path):
	c = D
	for p in path.split("."):
		c = c[p]
	return c
