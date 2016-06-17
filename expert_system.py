import os
import sys

# Global tab with authorised symbols
reserved = ['(',')', '|', '^', '!', '+', '<', '>', '=', '?']
ope_sym = ['(', '!', '+', '|', '^']
ope_sym_rev = ['^', '|', '+', '!', '(']

def usage():
	""" Return usage and quit the programme if the launch command is wrong"""
	if len(sys.argv) != 2:
		print("usage : {:s} <file>".format(sys.argv[0]))
		sys.exit()

def update_sym(c, solution, sym):
	"""
		symbols * bool * dict()
		update the symbols table
	"""
	if c in sym:
		if sym[c][0] == solution or sym[c][1] != True:
			sym[c] = [solution, True]
		else:
			print('Conflict !')
			exit()
		return sym[c][0]
	print('wrong symbol')
	exit()

#	COMMAND OR
def get_or(a, b):
	if type(a) == type(b) == bool:
		return a or b
	elif (type(a) == bool and a) or (type(b) == bool and b):
		return True
	return False

def solve_or(a, b, s, sym):
	if s:
		if type(a) == bool and not a:
			return solve_op(b, True, sym)
		elif type(b) == bool and not b:
			return solve_op(a, True, sym)
# END COMMAND OR

#	COMMAND XOR
def get_xor(a, b):
	return a != b

def solve_xor(a, b, s, sym):
	if type(a) == bool and s:
		return solve_op(b, not a, sym)
	if type(b) == bool and s:
		return solve_op(a, not b, sym)
#	END COMMAND XOR

#	COMMAND NOT
def get_not(a):
	return not a

def solve_not(a, s, sym):
	return solve_op(a, not s, sym)
# END COMMAND NOT

#	COMMAND AND
def get_and(a, b):
	return a and b

def solve_and(a, b, s, sym):
	if type(a) == bool and s:
		solve_op(a, True, sym)
	if type(b) == bool and s:
		solve_op(b, True, sym)
#	END COMMAND AND

#  COMAND IMPLY
def get_imply(a, b):
	if a == True:
		return True
	return False

#  COMMAND IF AND ONLY IF
def get_ssi(a, b):
	return False

# function tab to realise operation with facts
ope = {
	'|'	:get_or,
	'^'	:get_xor,
	'!'	:get_not,
	'+'	:get_and
}

# function tab to solves operation with facts and unknows
solve_ope = {
	'|'	:solve_or,
	'^'	:solve_xor,
	'!'	:solve_not,
	'+'	:solve_and
}

def do_op(s, sym): # do operation between booleans.
	"""
		list(str|bool) * dict(str: bool) -> list(str|bool)
		This is a recursive function which try to resolve facts
		then try to get new facts for finaly return the command
		The priority of operation is handle in this function
	"""
	for c in ope_sym: # loop to manage symbol by priority order
		index = get_occus(s, c)
		for i in index:
			if s[i] in ['^', '+'] and type(s[i - 1]) == type(s[i + 1]) == bool:
				s = s[0 : i - 1] + [ope[s[i]](s[i - 1], s[i + 1])] + s[i + 2:]
			elif s[i] == '|' and (type(s[i - 1]) == bool or type(s[i + 1]) == bool):
				s = s[0 : i - 1] + [ope[s[i]](s[i - 1], s[i + 1])] + s[i + 2:]
			elif s[i] == '!' and type(s[i + 1]) == bool:
				s = s[0 : i] + [ope[s[i]](s[i + 1])] + s[i + 2:]
			elif s[i] == '(' and type(s[i + 1]) == bool and s[i + 2] == ')':
				s = s[0 : i] + [s[i + 1]] + s[i + 3:]
			else:
				continue
			return do_op(s, sym) # if we go in a condition we restart processus frome th beginning
	if len(s) > 2 and s[1] == '=>' and s[0] == True: # try to solve the implication
		solve_op(s[2:], True, sym)
	elif len(s) > 2 and s[1] == '<=>' and s[0] == True: # try to solve the implication
		solve_op(s[2:], True, sym)
	elif len(s) > 2 and s[len(s) - 2] == '<=>' and s[len(s) - 1] == True: # try to solve the implication
		solve_op(s[0 : len(s) - 2], True, sym)
	return s

def solve_op(s, solution, sym):
	"""
		str * bool *
		solve operation
	"""
	s = do_op(s, sym)
	if len(s) == 1: # if the letter ca be assignable we assign it before move back in the stack
		if type(s[0]) != bool:
			return update_sym(s[0], solution, sym)
	for c in ope_sym_rev:
		index = get_occus_except(s, c)
		for i in index:
			if s[i] in ['|', '^', '+']:
				solve_ope[s[i]](s[0:i], s[i + 1:], solution, sym)
			elif s[i] == '!':
				solve_ope[s[i]](s[i + 1:], solution, sym)
			else:
				continue
			return s

def get_occus(s, c):
	""" return list of index occurences of c """
	i = 0
	tmp = 0
	res = []
	while len(s[i:]) > 0 and c in s[i:]:
		tmp = s[i:].index(c)
		res.append(i + tmp)
		i = i + tmp + 1
	return res

def get_occus_except(s, c):
	""" Same as get_occus but dont go in paranthesis """
	i = 0
	tmp = 0
	res = []
	while len(s[i:]) > 0 and c in s[i:]:
		tmp = s[i:].index(c)
		if '(' in s[i:tmp]:
			if ')' in s[i:]:
				i = len(s[i:]) - s[i:].reverse().index(')') - 1
				continue
			else:
				print('Error matching "(" ")"')
				exit()
		res.append(i + tmp)
		i = i + tmp + 1
	return res

def parser():
	"""
		None -> list(str)
		Delete comments and spaces from the file and return a list of instruction
	"""
	res = []
	try:
		f = open(sys.argv[1], 'r')
	except Exception as e:
		print(e)
		exit()
	s = f.readline()
	while s:
		s = ''.join(s.split())
		if '#' in s:
			com = s.index('#')
			s = s[:com]
			if len(s) > 0:
				res.append(s)
		elif len(s) > 0:
				res.append(s)
		s = f.readline()
	return res

def command_parser(s, symbols):
	"""
		str -> dict(str: bool)
		take a string with formulas and return it as split
	"""
	i = 0
	res = []
	while i < len(s):
		if s[i] == '<' and s[i:i + 3] == '<=>':
			res.append('<=>')
			i += 2
		elif s[i] == '=' and s[i:i + 2] == '=>':
			res.append('=>')
			i += 1
		else:
			res.append(s[i])
			if not s[i] in reserved:
				symbols.add(s[i])
		i += 1
	return res

def init_symbols(sym, fact):
	"""
		dict(str: bool) * list(str) -> dict(str: bool)
		return the symbols tab with facts initialized
	"""
	res = dict()
	for s in sym:
		if s in fact:
			res[s] = [True, True]
		else:
			res[s] = [False, False]
	return res

def replace_sym(cmd, sym):
	"""
		list(str) * dict(str: bool) -> list(str | bool)
		take command and symbols to return symbols replace by bool if it match with fact
	"""
	for i, c in enumerate(cmd):
		if c in sym and sym[c][1]:
			cmd[i] = sym[c][0]
	return cmd

def solver(cmds, sym):
	"""
		list(list(str)) * dict(str: bool) -> None
		take commands and symbols and solve the file
	"""
	for j in range(2):
		for i in range(len(cmds)):
			cmds[i] = do_op(cmds[i], sym)
			cmds[i] = replace_sym(cmds[i], sym)
			if len(cmds[i]) == 3 and type(cmds[i][0]) == type(cmds[i][2]) == bool and (cmds[i][1] == '=>' or cmds[i][1] == '<=>'):
				cmds.pop(i)
				return solver(cmds, sym)

def main():
	usage()
	symbols = set()
	cmds = []
	clean = parser()
	for cmd in clean:
		cmds.append(command_parser(cmd, symbols))
	facts = cmds[len(cmds) - 2]
	find = cmds[len(cmds) - 1]
	cmds = cmds[0:len(cmds) - 2]
	sym = init_symbols(symbols, facts)
	for cmd in cmds:
		replace_sym(cmd, sym)
	solver(cmds, sym)
	for i in find[1:]:
		print('{} : {}'.format(i, sym[i][0]))

if __name__ == '__main__':
	main()
