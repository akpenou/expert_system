from typing import Union, List, Dict, Optional, Type
import logging
import unittest
import sys
import os

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
logging.basicConfig(level = logging.DEBUG)
# ['<=>', '=>', '^', '|', '+']
# TreeElem = Union[Type[Node], Type[Leaf]]
# regex = ^\!?[A-Z]([\|\+\^]\!?[A-Z])*<?=>\!?[A-Z]([\|\+\^]\!?[A-Z])*$
TreeElem = int

def eval_imply(left: TreeElem, right: TreeElem) -> Optional[bool]:
    """ Evaluate the imply op.

    Args:
        left: left branch
        right: right branch

    Returns:
        return the comupation if it's possible esle none
    """
    if left.default():
        return None
    return True


def solve_imply(answer: bool, left: TreeElem, right: TreeElem):
    """ Solve the imply op.

    Args:
        left: left branch
        right: right branch

    Returns:
        return the comupation if it's possible esle none
    """
    if not left.default() and left.value():
        right.update(True)


def eval_equ(left: TreeElem, right: TreeElem) -> Optional[bool]:
    """ Evaluate the equ op.

    Args:
        left: left branch
        right: right branch

    Returns:
        return the comupation if it's possible esle none
    """
    solve_equ(True, left, right)
    if left.default() or right.default():
        return None
    return True


def solve_equ(answer: bool, left: TreeElem, right: TreeElem):
    """ Solve the equ op.

    Args:
        left: left branch
        right: right branch

    Returns:
        return the comupation if it's possible esle none
    """
    logging.debug('solve_equ {}'.format(answer))
    if not left.default():
        right.update(left.value())
    if not right.default():
        left.update(right.value())


def eval_and(left: TreeElem, right: TreeElem) -> Optional[bool]:
    """ Evaluate the and op.

    Args:
        left: left branch
        right: right branch

    Returns:
        return the comupation if it's possible esle none
    """
    logging.debug('eval_and')
    if not left.default() and not right.default():
        return left.value() and right.value()
    return None


def solve_and(answer: bool, left: TreeElem, right: TreeElem):
    """ Solve the and op.

    Args:
        left: left branch
        right: right branch

    Returns:
        return the comupation if it's possible esle none
    """
    logging.debug('solve_and {}'.format(answer))
    if answer:
        left.update(True)
        right.update(True)
    else:
        if not left.default() and left.value():
            right.update(False)
        if not right.default() and right.value():
            left.update(False)


def eval_or(left: TreeElem, right: TreeElem) -> Optional[bool]:
    """ Evaluate the or op.

    Args:
        left: left branch
        right: right branch

    Returns:
        return the  comupation if it's possible esle none
    """
    logging.debug('eval_or')
    if not left.default() and not right.default():
        return left.value() or right.value()
    if not left.default() and left.value():
        return True
    if not right.default() and right.value():
        return True
    return None


def solve_or(answer: bool, left: TreeElem, right: TreeElem):
    """ Solve the or op.

    Args:
        left: left branch
        right: right branch

    Returns:
        return the  comupation if it's possible esle none
    """
    logging.debug('solve_or {}'.format(answer))
    if answer:
        if not (left.default() or left.value()):
            right.update(True)
        if not (right.default() or right.value()):
            left.update(True)
    else:
        right.update(False)
        left.update(False)


def eval_xor(left: TreeElem, right: TreeElem) -> Optional[bool]:
    """ Evaluate the xor op.

    Args:
        left: left branch
        right: right branch

    Returns:
        return the  comupation if it's possible esle none
    """
    logging.debug('eval_xor')
    if not left.default() and not right.default():
        return left.value() != right.value()
    return None


def solve_xor(answer: bool, left: TreeElem, right: TreeElem):
    """ Solve the or op.

    Args:
        left: left branch
        right: right branch

    Returns:
        return the  comupation if it's possible esle none
    """
    logging.debug('solve_xor {}'.format(answer))
    if answer:
        if not left.default():
            right.update(not left.value())
        if not right.default():
            left.update(not right.value())
    else:
        if not left.default():
            right.update(left.value())
        if not right.default():
            left.update(right.value())

ops = {
        '<=>': {
            'eval': eval_equ,
            'solve': solve_equ
            },
        '=>': {
            'eval': eval_imply,
            'solve': solve_imply
            },
        '+': {
            'eval': eval_and,
            'solve': solve_and
            },
        '|': {
            'eval': eval_or,
            'solve': solve_or
            },
        '^': {
            'eval': eval_xor,
            'solve': solve_xor
            }
        }


class Symbol(object):
    """ Symbol """
    def __init__(self, letter: str):
        self.letter = letter
        self.__value = False
        self.__default = True

    def update(self, value: bool):
        if self.__default:
            self.__value = value
            self.__default = False
        if value != self.__value:
            raise ValueError('rule incoherence')

    def value(self):
        if self.__default:
            return None
        return self.__value

    def default(self):
        return self.__default

    def get_str(self):
        return [[str(self)]]

    def __str__(self):
        if self.__default:
            return str(self.letter)
        if self.__value:
            return OKGREEN + str(self.letter) + ENDC
        return FAIL + str(self.letter) + ENDC


class Node(object):
    """ Node in the equation tree.

    Attributes:
        op:
        left:
        right:
        size:
        deep:
    """

    def __init__(self, op: str, left: TreeElem, right: TreeElem, invert: bool = False):
        self.op = op
        self.left = left
        self.right = right
        self.__invert = invert
        self.__value = False
        self.__default = True

    def value(self):
        if self.__default:
            return self.eval()
        return self.__value

    def default(self):
        return self.__default

    def size(self):
        if self.default():
            return self.left.size() + self.right.size() + 1
        return 1

    def deep(self):
        return max(self.left.deep(), self.right.deep()) + 1

    def get_str(self):
        left_tab = self.left.get_str()
        right_tab = self.right.get_str()
        op = '\b!' if self.__invert else ''
        op += ('\b' if len(self.op) > 2 else '') + self.op
        if not self.__default:
            if self.__value:
                fusion = [[OKGREEN + op + ENDC]]
            else:
                fusion = [[FAIL + op + ENDC]]
        else:
            fusion = [[op]]
        for idx, item in enumerate(zip(left_tab, right_tab)):
            x, y = item
            fusion += [x + y]
        for item in left_tab[len(fusion) - 1:]:
            fusion += [item + [' '] * len(item)]
        for item in right_tab[len(fusion) - 1:]:
            fusion += [[' '] * len(item) + item]
        return fusion

    def solve(self, res: bool):
        self.left.eval()
        self.right.eval()
        logging.debug('solve')
        ops[self.op]['solve'](self.__invert != res, self.left, self.right)
        self.left.eval()
        self.right.eval()

    def eval(self):
        logging.debug('__eval {op}'.format(op = self.op))
        if not self.__default:
            return self.__value
        self.left.eval()
        self.right.eval()
        res = ops[self.op]['eval'](self.left, self.right)
        if res is not None:
            self.update(res)
        return res

    def update(self, value: bool):
        logging.debug('update {op} {val} {invert}'.format(op = self.op, val = value, invert = self.__invert != value))
        if self.__default:
            value = self.__invert != value
            self.__value = value
            self.__default = False
        print(self)
        if value != self.__value:
            raise ValueError('rule incoherence')
        self.solve(self.value())

    def __str__(self):
        elems = self.get_str()
        res = list()
        for idx, row in enumerate(elems):
            line = ''
            for node in row:
                line += '{spaces}{op}{spaces}'.format(
                        spaces = ' ' * (2 ** (self.deep() - idx) - 1),
                        op = node)
                line += ' '
            res.append(line)
        return '\n'.join(res)


class Leaf(object):
    """ Leaf in the equation tree.

        Attributes:
            symbol:
            size:
            deep:
            value:
            default:
    """
    def __init__(self, symbol, invert: bool = False): 
        self.symbol = symbol
        self.__invert = invert
        self.__value = False
        self.__default = True

    def deep(self):
        return 1

    def size(self):
        if self.default():
            return 1
        return 0

    def eval(self):
        return self.value()

    def value(self):
        return self.__invert != self.symbol.value()

    def default(self):
        return self.symbol.default()

    def update(self, value: bool):
        if self.__default:
            self.__value = value
            self.__default = False
            self.symbol.update(value)
        elif value != self.__value:
            raise ValueError('rule incoherence')

    def get_str(self):
        return [[('\b!' if self.__invert else '') + str(self)]]

    def __str__(self):
        return str(self.symbol)


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


def size(expr_forest: Optional[TreeElem]):
    """ compute the size the forest of expression.

    Args:
        expr_forest: the forest of expression parsed

    Returns:
        the size of the forest
    """
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
    new_size = size(expr_forest)
    while size != new_size:
        size = new_size
        for tree in expr_forest:
            tree.solve()
        new_size = size(expr_forest)


def repl(symbols: Symbol):
    """ The core function of the repl.

    Args:
        symbols: All symbols available
    """
    rules = list()
    while True:
        print('>>', end = ' ')
        txt_in = input().strip().lower()
        if txt_in in ['exit', 'quit', 'q']:
            print('bye')
            break
        elif txt_in.startswith('add '):
            add_rule(txt_in[4:], rules)
        elif txt_in in ['print', 'show']:
            print_rules(rules)
        elif txt_in == 'eval':
            expr_forest = make_tree(rules)
        elif txt_in == 'solve':
            solve(expr_forest)
        else:
            print('I don\'t understand the command')


if __name__ == '__main__':
    symbols = dict()
    for letter in [ chr(ascii_code) for ascii_code in range(ord('A'), ord('Z') + 1) ]:
        symbols[letter] = Symbol(letter)
    repl(symbols)
    # expression = lexer('A + B | C')
    # expression = lexer('A ^ B + C')
    # symbols = dict()
    # for letter in ['A', 'B', 'C', 'D', 'E' ]:
    #     symbols[letter] = Symbol(letter)
    # node_a = Node(Leaf(symbols['A']) , Leaf(symbols['B']))
    # node_b = Node(Leaf(symbols['C']) , Leaf(symbols['D']))
    # tree = Node(node_a, node_b)
