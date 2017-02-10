from typing import Union, List, Dict, Optional, Type
from classes import *
import parse
import logging
import unittest
import sys
import os

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
logging.basicConfig(level = logging.WARNING)
# ['<=>', '=>', '^', '|', '+']
# TreeElem = Union[Type[Node], Type[Leaf]]
# regex = ^\!?[A-Z]([\|\+\^]\!?[A-Z])*<?=>\!?[A-Z]([\|\+\^]\!?[A-Z])*$
TreeElem = int

def make_update(value: bool, keys: str, symbols):
    keys = keys.split(' ')
    for key in keys.strip().split(' '):
        if key in symbols:
            symbols[key].update(value)
        else:
            print('{:s} is not a valid symbol'.format(key))

def print_rules(rules: List[str]):
    """ Print all the rules.

    Args:
        rules: list of the rules to evaluate
    """
    for idx, rule in enumerate(rules):
        print(idx, ':', rule)


def add_rule(rule: str, rules: str):
    """ Add a rule to the list.

    Args:
        rule: the new rule to add and parse
        rules: list of the rules to evaluate

    Returns:
        the rules updated
    """
    rules.append(rule.upper())
    return rules


def compute_size(expr_forest: Optional[TreeElem]):
    """ compute the size the forest of expression.

    Args:
        expr_forest: the forest of expression parsed

    Returns:
        the size of the forest
    """
    if not expr_forest:
        return 0
    size = 0
    for tree in expr_forest:
        size += tree.size()
    return size


def solve(expr_forest: Optional[TreeElem]):
    """ Solve the forest of expression.

    Args:
        expr_forest: the forest of expression parsed
    """
    size = 0
    new_size = compute_size(expr_forest)
    while size != new_size:
        size = new_size
        for tree in expr_forest:
            tree.solve(True)
        new_size = compute_size(expr_forest)


def print_forest(expr_forest):
    if not expr_forest:
        print('Empty')
        return 
    for tree in expr_forest:
        print(tree)

def reset_symbols():
    symbols = dict()
    for letter in map(chr, range(ord('A'), ord('Z') + 1)):
        symbols[letter] = Symbol(letter)


def repl(symbols: Symbol):
    """ The core function of the repl.

    Args:
        symbols: All symbols available
    """
    rules = list()
    expr_forest = 0
    while True:
        print('>>', end = ' ')
        txt_in = input().strip().lower()
        if txt_in in ['exit', 'quit', 'q']:
            print('bye')
            break
        elif txt_in.startswith('add '):
            add_rule(txt_in[4:], rules)
        elif txt_in in ['print rules', 'show rules']:
            print_rules(rules)
        elif txt_in == 'eval':
            expr_forest = parse.make_tree(rules, symbols)
        elif txt_in == 'solve':
            solve(expr_forest)
        elif txt_in in ['print res']:
            print_forest(expr_forest)
        elif txt_in.startswith('True ') or txt_in.startswith('False '):
            value = txt_in.startswith('True ')
            make_update(
        elif txt_in in ['re
        else:
            print('I don\'t understand the command')


if __name__ == '__main__':
    symbols = symbols
    repl(symbols)
    # expression = lexer('A + B | C')
    # expression = lexer('A ^ B + C')
    # symbols = dict()
    # for letter in ['A', 'B', 'C', 'D', 'E' ]:
    #     symbols[letter] = Symbol(letter)
    # node_a = Node(Leaf(symbols['A']) , Leaf(symbols['B']))
    # node_b = Node(Leaf(symbols['C']) , Leaf(symbols['D']))
    # tree = Node(node_a, node_b)
