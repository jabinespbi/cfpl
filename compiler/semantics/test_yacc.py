import unittest

from compiler.semantics.state import State
from compiler.semantics.yacc import Yacc


class TestYacc(unittest.TestCase):
    def test_add_visible_rules(self):
        grammar = [
                ["<E>", "->", "<E>", "+", "<F>"],
                ["<E>", "->", "<F>"],
                ["<F>", "->", "+", "<F>"],
                ["<F>", "->", "<G>"],
                ["<G>", "->", "id"]
            ]

        # create first state
        state0 = State()
        # add rule to the state <CFPL>' -> . <CFPL>$
        e_dash = [grammar[0][0] + "'", "->", ".", grammar[0][0]]
        state0.rules.append(e_dash)
        Yacc.add_rules_with_nonterminal_followed_by_dot(state0, grammar)

        for rule in state0.rules:
            print(rule)


if __name__ == '__main__':
    unittest.main()
