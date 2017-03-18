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

def make_update(value: bool, keys: List[str], symbols):
    for key in map(lambda x: x.upper(), keys):
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
            tree.solve(None)
        new_size = compute_size(expr_forest)


def print_forest(expr_forest):
    """ Print the equation forest. """
    if not expr_forest:
        print('Empty')
        return 
    for tree in expr_forest:
        print(tree)


def reset_symbols():
    """ Reset all the symbols.

    Returns:
        all the symbols initialized
    """
    symbols = dict()
    for letter in map(chr, range(ord('A'), ord('Z') + 1)):
        symbols[letter] = Symbol(letter)
    return symbols


def init_forest(filename: str):
    """ Init the repl.

    Args:
        filename: name of the file to parse

    Returns:
        the rules, the expression forest, the values queries
    """
    symbols = reset_symbols()
    equations, init, queries = parse.parse_file(filename)
    expr_forest = parse.make_tree(equations, symbols)
    make_update(True, init, symbols)
    lst_queries = [ symbols[symbol] for symbol in queries ]
    return equations, expr_forest, lst_queries, symbols


def repl(filename: str, interactive: bool = False):
    """ The core function of the repl.

    Args:
        symbols: All symbols available
    """
    rules, expr_forest, queries, symbols = init_forest(filename)
    if not interactive:
        solve(expr_forest)
        for query in queries:
            print('{:s} => {}'.format(str(query), query.value()))
        exit()
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
        elif txt_in == 'solve':
            expr_forest = parse.make_tree(rules, symbols)
            solve(expr_forest)
        elif txt_in in ['print tree', 'show tree']:
            print_forest(expr_forest)
        elif txt_in.startswith('true '):
            keys = list(txt_in[5:].replace(' ', '').strip())
            make_update(True, keys, symbols)
        elif txt_in.startswith('false '):
            keys = list(txt_in[6:].replace(' ', '').strip())
            make_update(False, keys, symbols)
        elif txt_in in ['reset all']:
            rules, expr_forest, queries = init_forest(filename)
        elif txt_in in ['reset symbols']:
            symbols = reset_symbols()
        elif txt_in in ['help']:
            print('reset all|symbols')
            print('print|show rules')
            print('print|show tree')
            print('add [Rule]')
            print('True [Symbols]')
            print('False [Symbols]')
            print('solve')
        else:
            print('I don\'t understand the command')


if __name__ == '__main__':
    if len(sys.argv) not in [2, 3]:
        print('usage: python3 {:s} file [--interactive]'.format(sys.argv[0]))
        exit(os.EX_USAGE)
    filename = sys.argv[1]
    interactive = '--interactive' in sys.argv
    repl(filename, interactive)
    # expression = lexer('A + B | C')
    # expression = lexer('A ^ B + C')
    # symbols = dict()
    # for letter in ['A', 'B', 'C', 'D', 'E' ]:
    #     symbols[letter] = Symbol(letter)
    # node_a = Node(Leaf(symbols['A']) , Leaf(symbols['B']))
    # node_b = Node(Leaf(symbols['C']) , Leaf(symbols['D']))
    # tree = Node(node_a, node_b)
