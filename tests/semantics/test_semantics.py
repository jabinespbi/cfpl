import unittest

from compiler.semantics.grammar import Grammar
from compiler.semantics.yacc import Yacc


class TestTree(unittest.TestCase):
    # @unittest.skip("just manual")
    def test_traversal(self):
        lexemes = "* my first program in CFPL" + '\n' + \
                  "VAR abc, b, c AS INT" + '\n' + \
                  "VAR x, w_23='w' AS CHAR" + '\n' + \
                  "VAR t=\"TRUE\" AS BOOL" + '\n' + \
                  "START" + '\n' + \
                  "     abc=b=10 + 10   * 10 * (10 + 3) * (((3)))" + '\n' + \
                  "     w_23='a'" + '\n' + \
                  "     * this is a comment" + '\n' + \
                  "     OUTPUT: abc & \"hi\" & b & \"#\" & w_23 & \"[#]\"" + '\n' + \
                  "STOP" + '\n'
        yacc = Yacc(Grammar.get_grammar(), lexemes)
        yacc.create_parser()
        yacc.create_parsing_table()
        yacc.create_parse_tree()
        yacc.convert_parse_tree_to_abstract_syntax_tree()
        yacc.check_semantics()


if __name__ == '__main__':
    unittest.main()
