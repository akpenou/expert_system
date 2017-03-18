from typing import Union, List, Dict, Optional
import unittest
import logging
import sys
import os

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

TreeElem = int
Symbol = str

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
    if answer:
        left.solve(True)
    if not left.default() and left.value():
        right.solve(True)


def eval_equ(left: TreeElem, right: TreeElem) -> Optional[bool]:
    """ Evaluate the equ op.

    Args:
        left: left branch
        right: right branch

    Returns:
        return the comupation if it's possible esle none
    """
    solve_equ(None, left, right)
    if left.default() or right.default():
        return None
    return True


def solve_equ(answer: Optional[bool], left: TreeElem, right: TreeElem):
    """ Solve the equ op.

    Args:
        left: left branch
        right: right branch

    Returns:
        return the comupation if it's possible esle none
    """
    logging.debug('solve_equ {}'.format(answer))
    if not left.default():
        right.solve(left.value())
    if not right.default():
        left.solve(right.value())
    if not answer == None:
        right.solve(answer)
        left.solve(answer)
    


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
