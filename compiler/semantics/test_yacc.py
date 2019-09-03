import unittest

from compiler.semantics.yacc import Yacc


class TestYacc(unittest.TestCase):
    def test_check_exact(self):
        yacc = Yacc([
                ["<E>", "->", "<E>", "+", "<F>"],
                ["<E>", "->", "<F>"],
                ["<F>", "->", "+", "<G>"],
                ["<F>", "->", "<G>"],
                ["<G>", "->", "id"]
            ], "")




if __name__ == '__main__':
    unittest.main()
