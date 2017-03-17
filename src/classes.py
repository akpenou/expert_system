from typing import Union, List, Dict, Optional, Type
import logging
import ops

TreeElem = int
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

ops = {
        '<=>': {
            'eval': ops.eval_equ,
            'solve': ops.solve_equ
            },
        '=>': {
            'eval': ops.eval_imply,
            'solve': ops.solve_imply
            },
        '+': {
            'eval': ops.eval_and,
            'solve': ops.solve_and
            },
        '|': {
            'eval': ops.eval_or,
            'solve': ops.solve_or
            },
        '^': {
            'eval': ops.eval_xor,
            'solve': ops.solve_xor
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
            raise ValueError('rule incoherence: {:s} {} => {}'.format(self.letter, self.__value, value))

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
        if value != self.__value:
            raise ValueError('rule incoherence')
        #self.solve(self.value())

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
            raise ValueError('Error rule confilct')

    def solve(self, res: bool):
        self.update(self.__invert != res)

    def get_str(self):
        return [[('\b!' if self.__invert else '') + str(self)]]

    def __str__(self):
        return str(self.symbol)
