from transformer import g
import compiler
from pymeta.runtime import ParseError

class EscapeException(Exception):
	pass

class Test:

	def __init__(self, name, code, deps):
		self.name = name
		self.code = code
		self.deps = deps
		self.result = False
		self.message = self.name + ": Test didn't run"

	def run(self, grammar):
		self.message = self.name + ': '
		if self.code == '':
			self.message = self.message + 'No test set'
			return
		try:
			try:
				tree = str(compiler.parse(self.code))
			except SyntaxError:
				self.message = self.message + """Error in test.\n""" + self.code
				raise EscapeException()
			try:
				matcher = grammar(tree)
				generated = matcher.apply('any')
			except ParseError:
				self.message = self.message + """Error in grammar.\n""" + self.code + """\n\n""" + tree
				raise EscapeException()
			try:
				assert str(compiler.parse(generated)) == tree
			except AssertionError:
				self.message = self.message + """Error, generated code does not match original.\n""" + self.code + """\n\n""" + tree + """\n\n""" + generated
				raise EscapeException()
			except SyntaxError:
				self.message = self.message + """Error in generated code.\n""" + self.code + """\n\n""" + tree + """\n\n""" + generated
				raise EscapeException()
			self.message = self.message + "OK"
			self.result = True
		except EscapeException:
			pass

tests = [\
	Test('Addition','1+2', ['Constant']), \
	Test('And', '1 and True', ['Name', 'Constant']), \
	Test('Assign Attribute', '', []), \
	Test('Assign Name', 'x = 10', ['Name', 'Constant', 'Assign']), \
	Test('Assign Tuple', 'x, y, z = 1, 2, "10"', ['Tuple', 'Name', 'Constant', 'Assign']), \
	Test('Assert', 'assert 10 < 9', ['Compare', 'Constant']), \
	Test('Assign', 'x = y = 10', ['Name', 'Constant']), \
	Test('Augmenting Assign', 'x += 10', ['Statement']), \
	Test('Backquote', '', ['Statement']), \
	Test('Bitwise And', '', ['Statement']), \
	Test('Bitwise Or', '', ['Statement']), \
	Test('Bitwise Exclusive Or', '', ['Statement']), \
	Test('Break', '', ['Statement']), \
	Test('Function Call', 'str(x)', ['Statement']), \
	Test('Class', """class A(object):
	def __init__(self):
		pass

class B(A):

	def __init__(self):
		pass""", ['Statement']), \
	Test('Compare', 'x < y and 1 == 5 and 2 > 8', ['Name', 'Constant', 'And']), \
	Test('Constant', '1', []), \
	Test('Continue', '', ['Statement']), \
	Test('Decorators', '', ['Statement']), \
	Test('Dictionary', """x = 5
a = "s"
y = {a:1, 5:x}""", ['Statement']), \
	Test('Discard', '5', ['Statement']), \
	Test('Division', 'x/10', ['Name', 'Constant']), \
	Test('Ellipsis', '', ['Statement']), \
	Test('Expression', '', ['Statement']), \
	Test('Execute', 'exec("x=True")', ['Statement']), \
	Test('Rounded-Down Division', '', ['Statement']), \
	Test('For Loop', """for x in range(5):
	print str(x)""", ['Statement']), \
	Test('From', """from os import get_cwd
from sys import exit as Exit
from pygame import draw, mixer as sound, surface""", ['Statement']), \
	Test('Function', """def f(x, y=False, z="TEST", a="ING"):
	if y:
		print x
""", ['Statement']), \
	Test('GenExpr', '', ['Statement']), \
	Test('GenExprFor', '', ['Statement']), \
	Test('GenExprIf', '', ['Statement']), \
	Test('GenExprInner', '', ['Statement']), \
	Test('Get Attribute', 'x.name', ['Statement']), \
	Test('Global', """global x
x = 2""", ['Statement']), \
	Test('If', """if x < 2:
	print "a"
elif x > 2:
	print "b"
elif x == 2:
	print "c"
else:
	print 'd'""", ['Statement']), \
	Test('Import', """import os
import sys as System""", ['Statement']), \
	Test('Keyword', '', ['Statement']), \
	Test('Lambda', '', ['Statement']), \
	Test('Left Shift', '', ['Statement']), \
	Test('List', '[1,2,3,[1,2,"s"]]', ['Statement']), \
	Test('List Comprehension', '', ['Statement']), \
	Test('List Comprehension For', '', ['Statement']), \
	Test('List Comprehension If', '', ['Statement']), \
	Test('Modulo', '10%3', ['Statement']), \
	Test('Module', 'True', ['Statement', 'Name']), \
	Test('Multiplication', '5*x', ['Constant', 'Name']), \
	Test('Name', 'True', ['Constant']), \
	Test('Not', 'not True', ['Statement']), \
	Test('Or', '2<5 or True', ['Statement']), \
	Test('Pass', 'pass', ['Statement']), \
	Test('Power', '5**0.2', ['Statement']), \
	Test('Print Inline', 'print "TEST",', ['Statement']), \
	Test('Print New Line', 'print "TEST"', ['Statement']), \
	Test('Raise', 'raise ValueError()', ['Statement']), \
	Test('Return', """def f(x):
	return x*x""", ['Statement']), \
	Test('Right Shift', '', ['Statement']), \
	Test('Slice', """x[5:15]
y[:10]
z[a:]""", ['Statement']), \
	Test('Slice Object', '', ['Statement']), \
	Test('Statement', 'True', ['Module', 'Name']), \
	Test('Subtraction', '1-x', ['Constant', 'Name']), \
	Test('Subscription', '', ['Statement']), \
	Test('Try Except', """try:
	[0,1,2].remove(5)
except ValueError:
	print "No 5"
except SyntaxError, e:
	print "Syntax Error: "+str(e)
except:
	print 'Other Error'""", ['Statement']), \
	Test('Try Finally', """try:
	print "x"
except:
	print "y"
finally:
	print 'z'""", ['Statement']), \
	Test('Tuple', '(a, b, (c, d))', ['Name']), \
	Test('Unary Addition', '', ['Statement']), \
	Test('Unary Subtraction', '-10', ['Statement']), \
	Test('While Loop', """x = 1
while x < 5:
	print str(x)
	x += 1""", ['Statement']), \
	Test('With', '', ['Statement']), \
	Test('Yield', '', ['Statement']) \
]

for test in tests:
	test.run(g)

failed = []
succeeded = []
unknown = []

for test in tests:
	if not test.result:
		failed.append(test)
	else:
		succeeded.append(test)

for test in failed[:]:
	for dep in test.deps:
		for test2 in failed[:]:
			if test2.name == dep:
				try:
					failed.remove(test)
					unknown.append(test)
				except ValueError:
					pass

for s in succeeded:
	print s.message

for u in unknown:
	print u.name + ': Unknown (depends on broken rules)'

for f in failed:
	print f.message