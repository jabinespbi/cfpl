import unittest

from compiler.semantics.action_type import ActionType
from compiler.semantics.grammar import Grammar
from compiler.semantics.state import State
from compiler.semantics.yacc import Yacc


class TestYacc(unittest.TestCase):
    def create_sample_grammar(self):
        return [
            ["<E>", "->", "<E>", "+", "<F>"],
            ["<E>", "->", "<F>"],
            ["<F>", "->", "+", "<F>"],
            ["<F>", "->", "<G>"],
            ["<G>", "->", "id"]
        ]

    def test_add_visible_rules(self):
        grammar = self.create_sample_grammar()
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
        grammar = self.create_sample_grammar()
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

    @unittest.skip("prints a long message")
    def test_create_parser_for_cflp(self):
        yacc = Yacc(Grammar.get_grammar(), "")
        yacc.create_parser()

        i = 0
        for state in yacc.parser_states:
            print("\nState" + str(i))
            i += 1
            for rule in state.rules:
                print(rule)

    @unittest.skip("prints a long message")
    def test_create_parsing_table_for_cflp(self):
        yacc = Yacc(Grammar.get_grammar(), "")
        yacc.create_parser()
        yacc.create_parsing_table()

        for x in yacc.slr1:
            print("\nState" + str(x))
            for y in yacc.slr1[x]:
                action = yacc.slr1[x][y]
                if y is '\n':
                    msg = "'\\n'" + ": "
                else:
                    msg = "'" + y + "'" + ": "
                if action is not None:
                    msg += "[" + action.type.name + "]" + " state[" + str(action.next_state) + "]"
                    if action.type is ActionType.REDUCE:
                        msg += "reduce[" + str(action.reduce_rule) + "]"
                else:
                    msg += "None"
                print(msg)

    def test_create_parsing_table(self):
        grammar = self.create_sample_grammar()
        yacc = Yacc(grammar, "")
        yacc.create_parser()
        yacc.create_parsing_table()

        self.assertEqual(yacc.slr1[0]["+"].type, ActionType.SHIFT)
        self.assertEqual(yacc.slr1[0]["+"].next_state, 3)
        self.assertEqual(yacc.slr1[0]["id"].type, ActionType.SHIFT)
        self.assertEqual(yacc.slr1[0]["id"].next_state, 5)
        self.assertEqual(yacc.slr1[0]["EoI"], None)
        self.assertEqual(yacc.slr1[0]["<E>"].type, ActionType.GOTO)
        self.assertEqual(yacc.slr1[0]["<E>"].next_state, 1)
        self.assertEqual(yacc.slr1[0]["<F>"].type, ActionType.GOTO)
        self.assertEqual(yacc.slr1[0]["<F>"].next_state, 2)
        self.assertEqual(yacc.slr1[0]["<G>"].type, ActionType.GOTO)
        self.assertEqual(yacc.slr1[0]["<G>"].next_state, 4)

        self.assertEqual(yacc.slr1[1]["+"].type, ActionType.SHIFT)
        self.assertEqual(yacc.slr1[1]["+"].next_state, 6)
        self.assertEqual(yacc.slr1[1]["id"], None)
        self.assertEqual(yacc.slr1[1]["EoI"].type, ActionType.ACCEPT)
        self.assertEqual(yacc.slr1[1]["<E>"], None)
        self.assertEqual(yacc.slr1[1]["<F>"], None)
        self.assertEqual(yacc.slr1[1]["<G>"], None)

        self.assertEqual(yacc.slr1[2]["+"].type, ActionType.REDUCE)
        self.assertEqual(yacc.slr1[2]["+"].reduce_rule, ["<E>", "->", "<F>"])
        self.assertEqual(yacc.slr1[2]["id"], None)
        self.assertEqual(yacc.slr1[2]["EoI"].type, ActionType.REDUCE)
        self.assertEqual(yacc.slr1[2]["EoI"].reduce_rule, ["<E>", "->", "<F>"])
        self.assertEqual(yacc.slr1[2]["<E>"], None)
        self.assertEqual(yacc.slr1[2]["<F>"], None)
        self.assertEqual(yacc.slr1[2]["<G>"], None)

        self.assertEqual(yacc.slr1[3]["+"].type, ActionType.SHIFT)
        self.assertEqual(yacc.slr1[3]["+"].next_state, 3)
        self.assertEqual(yacc.slr1[3]["id"].type, ActionType.SHIFT)
        self.assertEqual(yacc.slr1[3]["id"].next_state, 5)
        self.assertEqual(yacc.slr1[3]["EoI"], None)
        self.assertEqual(yacc.slr1[3]["<E>"], None)
        self.assertEqual(yacc.slr1[3]["<F>"].type, ActionType.GOTO)
        self.assertEqual(yacc.slr1[3]["<F>"].next_state, 7)
        self.assertEqual(yacc.slr1[3]["<G>"].type, ActionType.GOTO)
        self.assertEqual(yacc.slr1[3]["<G>"].next_state, 4)

        self.assertEqual(yacc.slr1[4]["+"].type, ActionType.REDUCE)
        self.assertEqual(yacc.slr1[4]["+"].reduce_rule, ["<F>", "->", "<G>"])
        self.assertEqual(yacc.slr1[4]["id"], None)
        self.assertEqual(yacc.slr1[4]["EoI"].type, ActionType.REDUCE)
        self.assertEqual(yacc.slr1[4]["EoI"].reduce_rule, ["<F>", "->", "<G>"])
        self.assertEqual(yacc.slr1[4]["<E>"], None)
        self.assertEqual(yacc.slr1[4]["<F>"], None)
        self.assertEqual(yacc.slr1[4]["<G>"], None)

        self.assertEqual(yacc.slr1[5]["+"].type, ActionType.REDUCE)
        self.assertEqual(yacc.slr1[5]["+"].reduce_rule, ["<G>", "->", "id"])
        self.assertEqual(yacc.slr1[5]["id"], None)
        self.assertEqual(yacc.slr1[5]["EoI"].type, ActionType.REDUCE)
        self.assertEqual(yacc.slr1[5]["EoI"].reduce_rule, ["<G>", "->", "id"])
        self.assertEqual(yacc.slr1[5]["<E>"], None)
        self.assertEqual(yacc.slr1[5]["<F>"], None)
        self.assertEqual(yacc.slr1[5]["<G>"], None)

        self.assertEqual(yacc.slr1[6]["+"].type, ActionType.SHIFT)
        self.assertEqual(yacc.slr1[6]["+"].next_state, 3)
        self.assertEqual(yacc.slr1[6]["id"].type, ActionType.SHIFT)
        self.assertEqual(yacc.slr1[6]["id"].next_state, 5)
        self.assertEqual(yacc.slr1[6]["EoI"], None)
        self.assertEqual(yacc.slr1[6]["<E>"], None)
        self.assertEqual(yacc.slr1[6]["<F>"].type, ActionType.GOTO)
        self.assertEqual(yacc.slr1[6]["<F>"].next_state, 8)
        self.assertEqual(yacc.slr1[6]["<G>"].type, ActionType.GOTO)
        self.assertEqual(yacc.slr1[6]["<G>"].next_state, 4)

        self.assertEqual(yacc.slr1[7]["+"].type, ActionType.REDUCE)
        self.assertEqual(yacc.slr1[7]["+"].reduce_rule, ["<F>", "->", "+", "<F>"])
        self.assertEqual(yacc.slr1[7]["id"], None)
        self.assertEqual(yacc.slr1[7]["EoI"].type, ActionType.REDUCE)
        self.assertEqual(yacc.slr1[7]["EoI"].reduce_rule, ["<F>", "->", "+", "<F>"])
        self.assertEqual(yacc.slr1[7]["<E>"], None)
        self.assertEqual(yacc.slr1[7]["<F>"], None)
        self.assertEqual(yacc.slr1[7]["<G>"], None)

        self.assertEqual(yacc.slr1[8]["+"].type, ActionType.REDUCE)
        self.assertEqual(yacc.slr1[8]["+"].reduce_rule, ["<E>", "->", "<E>", "+", "<F>"])
        self.assertEqual(yacc.slr1[8]["id"], None)
        self.assertEqual(yacc.slr1[8]["EoI"].type, ActionType.REDUCE)
        self.assertEqual(yacc.slr1[8]["EoI"].reduce_rule, ["<E>", "->", "<E>", "+", "<F>"])
        self.assertEqual(yacc.slr1[8]["<E>"], None)
        self.assertEqual(yacc.slr1[8]["<F>"], None)
        self.assertEqual(yacc.slr1[8]["<G>"], None)

    def test_create_parse_tree_for_cfpl(self):
        lexemes = "* my first program in CFPL" + '\n' + \
                  "VAR abc, b, c AS INT" + '\n' + \
                  "VAR x, w_23='w' AS CHAR" + '\n' + \
                  "VAR t=\"TRUE\" AS BOOL" + '\n' + \
                  "START" + '\n' + \
                  "     abc=b=10" + '\n' + \
                  "     w_23='a'" + '\n' + \
                  "     * this is a comment" + '\n' + \
                  "     OUTPUT: abc & \"hi\" & b & \"#\" & w_23 & \"[#]\"" + '\n' + \
                  "STOP" + '\n'
        yacc = Yacc(Grammar.get_grammar(), lexemes)
        yacc.create_parser()
        yacc.create_parsing_table()
        yacc.create_parse_tree()

    # @unittest.skip("just a long message, manual testing")
    def test_convert_to_abstract_syntax_tree_cfpl1(self):
        lexemes = "* my first program in CFPL" + '\n' + \
                  "VAR abc, b, c AS INT" + '\n' + \
                  "VAR x, w_23='w' AS CHAR" + '\n' + \
                  "VAR t=\"TRUE\" AS BOOL" + '\n' + \
                  "START" + '\n' + \
                  "     abc=b=10 + 10   * 10 * (10 + 2) * (((3)))" + '\n' + \
                  "     w_23='a'" + '\n' + \
                  "     * this is a comment" + '\n' + \
                  "     OUTPUT: abc & \"hi\" & b & \"#\" & w_23 & \"[#]\"" + '\n' + \
                  "STOP" + '\n'
        yacc = Yacc(Grammar.get_grammar(), lexemes)
        yacc.create_parser()
        yacc.create_parsing_table()
        yacc.create_parse_tree()
        yacc.convert_parse_tree_to_abstract_syntax_tree()

    @unittest.skip("just a long message, manual testing")
    def test_convert_to_abstract_syntax_tree_cfpl2(self):
        lexemes = "* my first program in CFPL" + '\n' + \
                  "START" + '\n' + \
                  "     abc=b=10 + 10   * 10 * (10 + 2) * (((3)))" + '\n' + \
                  "     w_23='a'" + '\n' + \
                  "     * this is a comment" + '\n' + \
                  "     OUTPUT: abc & \"hi\" & b & \"#\" & w_23 & \"[#]\"" + '\n' + \
                  "STOP" + '\n'
        yacc = Yacc(Grammar.get_grammar(), lexemes)
        yacc.create_parser()
        yacc.create_parsing_table()
        yacc.create_parse_tree()
        yacc.convert_parse_tree_to_abstract_syntax_tree()

    @unittest.skip("just a long message, manual testing")
    def test_convert_to_abstract_syntax_tree_cfpl3(self):
        lexemes = "* my first program in CFPL" + '\n' + \
                  "VAR abc, b, c AS INT" + '\n' + \
                  "VAR x, w_23='w' AS CHAR" + '\n' + \
                  "VAR t=\"TRUE\" AS BOOL" + '\n'
        yacc = Yacc(Grammar.get_grammar(), lexemes)
        yacc.create_parser()
        yacc.create_parsing_table()
        yacc.create_parse_tree()
        yacc.convert_parse_tree_to_abstract_syntax_tree()

    @unittest.skip("just a long message, manual testing")
    def test_convert_to_abstract_syntax_tree_cfpl4(self):
        lexemes = "* my first program in CFPL" + '\n' + \
                  "VAR abc, b, c AS INT" + '\n' + \
                  "VAR x, w_23='w' AS CHAR" + '\n' + \
                  "VAR t=\"TRUE\" AS BOOL" + '\n' + \
                  "START" + '\n' + \
                  "STOP" + '\n'
        yacc = Yacc(Grammar.get_grammar(), lexemes)
        yacc.create_parser()
        yacc.create_parsing_table()
        yacc.create_parse_tree()
        yacc.convert_parse_tree_to_abstract_syntax_tree()
        print()


if __name__ == '__main__':
    unittest.main()
