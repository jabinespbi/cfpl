import unittest

from compiler.semantics.yacc import Yacc


class TestYacc(unittest.TestCase):
    def test_check_exact(self):
        yacc = Yacc("")

        for rule in yacc.state.rules:
            print(rule)


if __name__ == '__main__':
    unittest.main()
