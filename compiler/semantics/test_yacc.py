import unittest

from compiler.semantics.grammar import Grammar
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

        yacc = Yacc(grammar, "")

        # create first state
        state0 = State()
        # add rule to the state <CFPL>' -> . <CFPL>$
        e_dash = [grammar[0][0] + "'", "->", ".", grammar[0][0]]
        state0.rules.append(e_dash)
        yacc.add_rules_with_nonterminal_followed_by_dot(state0)

        expected = [
                    ["<E>'", '->', '.', '<E>'],
                    ['<E>', '->', '.', '<E>', '+', '<F>'],
                    ['<E>', '->', '.', '<F>'],
                    ['<F>', '->', '.', '+', '<F>'],
                    ['<F>', '->', '.', '<G>'],
                    ['<G>', '->', '.', 'id'],
                ]
        self.assertEqual(state0.rules, expected)

    def test_create_parser(self):
        grammar = [
                ["<E>", "->", "<E>", "+", "<F>"],
                ["<E>", "->", "<F>"],
                ["<F>", "->", "+", "<F>"],
                ["<F>", "->", "<G>"],
                ["<G>", "->", "id"]
            ]

        yacc = Yacc(grammar, "")
        yacc.create_parser()
        state0 = yacc.parser_states[0]
        expected_state0_rules = [
            ["<E>'", "->", ".", "<E>"],
            ["<E>", "->", ".", "<E>", "+", "<F>"],
            ["<E>", "->", ".", "<F>"],
            ["<F>", "->", ".", "+", "<F>"],
            ["<F>", "->", ".", "<G>"],
            ["<G>", "->", ".", "id"],
        ]

        self.assertEqual(state0.rules, expected_state0_rules)
        self.assertEqual(len(state0.transitions), 5)
        self.assertEqual(state0.transitions[0].state, yacc.parser_states[1])
        self.assertEqual(state0.transitions[0].transition_input, '<E>')
        self.assertEqual(state0.transitions[1].state, yacc.parser_states[2])
        self.assertEqual(state0.transitions[1].transition_input, '<F>')
        self.assertEqual(state0.transitions[2].state, yacc.parser_states[3])
        self.assertEqual(state0.transitions[2].transition_input, '+')
        self.assertEqual(state0.transitions[3].state, yacc.parser_states[4])
        self.assertEqual(state0.transitions[3].transition_input, '<G>')
        self.assertEqual(state0.transitions[4].state, yacc.parser_states[5])
        self.assertEqual(state0.transitions[4].transition_input, 'id')

        state1 = yacc.parser_states[1]
        expected_state1_rules = [
            ["<E>'", '->', '<E>', '.'],
            ['<E>', '->', '<E>', '.', '+', '<F>']
        ]

        self.assertEqual(state1.rules, expected_state1_rules)
        self.assertEqual(len(state1.transitions), 1)
        self.assertEqual(state1.transitions[0].state, yacc.parser_states[6])
        self.assertEqual(state1.transitions[0].transition_input, '+')

        state2 = yacc.parser_states[2]
        expected_state2_rules = [
            ['<E>', '->', '<F>', '.']
        ]

        self.assertEqual(state2.rules, expected_state2_rules)
        self.assertEqual(len(state2.transitions), 0)

        state3 = yacc.parser_states[3]
        expected_state3_rules = [
            ['<F>', '->', '+', '.', '<F>'],
            ['<F>', '->', '.', '+', '<F>'],
            ['<F>', '->', '.', '<G>'],
            ['<G>', '->', '.', 'id'],
        ]

        self.assertEqual(state3.rules, expected_state3_rules)
        self.assertEqual(len(state3.transitions), 4)
        self.assertEqual(state3.transitions[0].state, yacc.parser_states[7])
        self.assertEqual(state3.transitions[0].transition_input, '<F>')
        self.assertEqual(state3.transitions[1].state, yacc.parser_states[3])
        self.assertEqual(state3.transitions[1].transition_input, '+')
        self.assertEqual(state3.transitions[2].state, yacc.parser_states[4])
        self.assertEqual(state3.transitions[2].transition_input, '<G>')
        self.assertEqual(state3.transitions[3].state, yacc.parser_states[5])
        self.assertEqual(state3.transitions[3].transition_input, 'id')

        state4 = yacc.parser_states[4]
        expected_state4_rules = [
            ['<F>', '->', '<G>', '.']
        ]

        self.assertEqual(state4.rules, expected_state4_rules)
        self.assertEqual(len(state4.transitions), 0)

        state5 = yacc.parser_states[5]
        expected_state5_rules = [
            ['<G>', '->', 'id', '.']
        ]

        self.assertEqual(state5.rules, expected_state5_rules)
        self.assertEqual(len(state5.transitions), 0)

        state6 = yacc.parser_states[6]
        expected_state6_rules = [
            ['<E>', '->', '<E>', '+', '.', '<F>'],
            ['<F>', '->', '.', '+', '<F>'],
            ['<F>', '->', '.', '<G>'],
            ['<G>', '->', '.', 'id'],
        ]

        self.assertEqual(state6.rules, expected_state6_rules)
        self.assertEqual(len(state6.transitions), 4)
        self.assertEqual(state6.transitions[0].state, yacc.parser_states[8])
        self.assertEqual(state6.transitions[0].transition_input, '<F>')
        self.assertEqual(state6.transitions[1].state, yacc.parser_states[3])
        self.assertEqual(state6.transitions[1].transition_input, '+')
        self.assertEqual(state6.transitions[2].state, yacc.parser_states[4])
        self.assertEqual(state6.transitions[2].transition_input, '<G>')
        self.assertEqual(state6.transitions[3].state, yacc.parser_states[5])
        self.assertEqual(state6.transitions[3].transition_input, 'id')

        state7 = yacc.parser_states[7]
        expected_state7_rules = [
            ['<F>', '->', '+', '<F>', '.']
        ]

        self.assertEqual(state7.rules, expected_state7_rules)
        self.assertEqual(len(state7.transitions), 0)

        state8 = yacc.parser_states[8]
        expected_state8_rules = [
            ['<E>', '->', '<E>', '+', '<F>', '.']
        ]

        self.assertEqual(state8.rules, expected_state8_rules)
        self.assertEqual(len(state8.transitions), 0)

    def test_create_parser_for_cflp(self):
        yacc = Yacc(Grammar.get_grammar(), "")
        yacc.create_parser()

        for state in yacc.parser_states:
            print("\nNew State -------------------")
            for rule in state.rules:
                print(rule)

if __name__ == '__main__':
    unittest.main()
