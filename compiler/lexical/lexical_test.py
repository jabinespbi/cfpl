import os
import unittest

from compiler.lexical.lexical import Lexical


class TestLexical(unittest.TestCase):
    lexemes = "* my first program in CFPL" + '\n' + \
              "VAR abc, b, c AS INT" + '\n' +  \
              "VAR x, w_23='w' AS CHAR" + '\n' +  \
              "VAR t=\"TRUE\" AS BOOL" + '\n' +  \
              "START" + '\n' +  \
              "     abc=b=10" + '\n' +  \
              "     w_23='a'" + '\n' +  \
              "     * this is a comment" + '\n' +  \
              "     OUTPUT: abc & \"hi\" & b & \"#\" & w_23 & \"[#]\"" + '\n' +  \
              "STOP" + '\n'

    def setUp(self) -> None:
        self.lexical = Lexical(self.lexemes)

    def tearDown(self) -> None:
        del self.lexical

    # multiple assert to avoid the test taking so long
    def test_tokens(self):
        token = self.lexical.next()
        self.assertEqual('VAR', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('abc', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual(',', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('b', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual(',', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('c', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('AS', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('INT', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('\n', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('VAR', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('x', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual(',', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('w_23', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('=', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('\'w\'', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('AS', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('CHAR', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('\n', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('VAR', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('t', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('=', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('"TRUE"', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('AS', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('BOOL', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('\n', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('START', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('\n', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('abc', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('=', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('b', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('=', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('10', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('\n', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('w_23', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('=', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('\'a\'', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('\n', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('OUTPUT:', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('abc', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('&', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('"hi"', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('&', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('b', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('&', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('"#"', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('&', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('w_23', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('&', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('"[#]"', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('\n', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('STOP', self.lexemes[token[0]: token[1]])

        token = self.lexical.next()
        self.assertEqual('\n', self.lexemes[token[0]: token[1]])


if __name__ == '__main__':
    unittest.main()
