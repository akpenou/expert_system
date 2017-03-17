from typing import Union, List, Dict, Optional, Type
from classes import *
import logging
import os
import re

TreeElem = int
Symbol = int

def find_token(tokens: List[str], get: str) -> Optional[int]:
    """ Find token without search in prenthesis.

    Args:
        tokens: tokens of the expression
        get: token to find
        
    Returns:
        Index of the token else None
    """
    count = 0
    for idx, token in enumerate(tokens):
        if token == '(':
            count += 1
        if token == ')':
            count -= 1
            if count < 0:
                raise ValueError('Bad Globing')
        if token == get and not count:
            return idx
    return None


def tokenize_wchr(tokens: List[str], get: str):
    """ Merge large tokens in list.

    Args:
        tokens: tokens of the expression
        get: new token to merge
    
    Returns:
        list of token merge.
    """
    idx = tokens.index(get[0])
    if idx + len(get) > len(tokens):
        raise ValueError('Wrong token')
    if get != ''.join(tokens[idx:idx + len(get)]):
        raise ValueError('Wrong token')
    tokens = tokens[:idx] + [get] + tokens[idx + len(get):]
    return tokens


def result_parenthesis(tokens: List[str]):
    """ Find if the expression is a res of parenthesis.

    Args:
        tokens: tokens to evaluate

    Returns:
        True if wew can delete parenthesis
    """
    if len(tokens) <= 2 or tokens[0] != '(' or tokens[-1] != ')':
        return False
    count = 0
    for idx, token in enumerate(tokens[1:-1]):
        if token == '(':
            count += 1
        if token == ')':
            count -= 1
            if count < 0:
                return False
    return count == 0


def lexer(expression: str) -> List[str]:
    """ Lexer to get token expression.

    Args:
        expression: expression made by the user

    Returns:
        list of tokens
    """
    tokens = list(expression.strip().replace(' ', ''))
    while '<' in tokens:
        tokens = tokenize_wchr(tokens, '<=>')
    while '=' in tokens:
        tokens = tokenize_wchr(tokens, '=>')
    return tokens


def parser(tokens: List[str], symbols: Dict[str, object], invert: bool = False):
    """ Expression parser.

    Args:
        tokens: tokens of the expression
        symbols: All symbols available

    Returns:
        The tree expression
    """
    if result_parenthesis(tokens):
        tokens = tokens[1:-1]
    if not len(tokens):
        return None
    for operator in ['<=>', '=>', '^', '|', '+']:
        idx = find_token(tokens, operator)
        if not idx:
            continue
        logging.debug('{} : {}'.format(tokens[:idx], tokens[idx + 1:]))
        return Node(tokens[idx], parser(tokens[:idx], symbols),\
                     parser(tokens[idx + 1:], symbols),\
                                         invert)
    if tokens[0] == '!':
        return parser(tokens[1:], symbols, True)
    if len(tokens) == 1 and tokens[0] in symbols:
        return Leaf(symbols[tokens[0]], invert)
    logging.warning(tokens)
    raise ValueError('Wrong input rule')


def make_tree(expressions: List[str], symbols: Symbol):
    """ Return a big tree with all the rules.

    Args:
        expressions: the expressions to parse
        symbols: All symbols available

    Returns:
        a expression tree
    """
    res = list()
    for expression in expressions:
        tokens = lexer(expression)
        tree = parser(tokens, symbols)
        res.append(tree)
    return res

def parse_file(filename: str):
    """ Parse the file.

    Args:
        filename: name of the file to parse

    Returns:
        (equations of the file, symbols to true, symbols to find)
    """
    try:
        f = open(filename)
        lines = f.readlines()
    except Exception as e:
        print('Error in open for file:', e)
        exit(os.EX_DATAERR)
    remove_comment = lambda line: line[:line.index('#')].strip() if '#' in line else line
    exists = lambda line: len(line.strip())
    lines = list(filter(exists, map(remove_comment, lines)))
    for line in lines:
        print(line)
    if not (len(lines) > 2 and lines[-1].startswith('?') and lines[-2].startswith('=')):
        print('Error invalid file')
        exit(os.EX_DATAERR)
    equations = lines[:-2]
    init = lines[-2].strip()
    queries = lines[-1].strip()
    if not (re.fullmatch('\=[A-Z]*', init) and re.fullmatch('\?[A-Z]*', queries)):
        print('Error invalid file')
        exit(os.EX_DATAERR)
    return equations, list(init[1:]), list(queries[1:])
