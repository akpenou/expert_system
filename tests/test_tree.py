from ../src import tree
import unittest

class TestSymbol(unittest.TestCase):

    def test_initialization(self):
        symbols = dict()
        for letter in ['T', 'F', 't', 'f']:
            symbols[letter] = Symbol(letter)
        self.assert
        symbols['T'].set_value(True)
        symbols['F'].set_value(False)

        
        
