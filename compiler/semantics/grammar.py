import copy


class Grammar:
    """The grammar and its rules"""

    @staticmethod
    def find_rule_and_deep_copy(lhs, grammar):
        productions = []
        for rule in grammar:
            if rule[0] == lhs:
                productions.append(rule)

        return copy.deepcopy(productions)

    @staticmethod
    def get_grammar():
        return [
            ["<cfpl>", "->", "<declaration-list>", "<main-block>"],
            ["<cfpl>", "->", "<declaration-list>"],
            ["<cfpl>", "->", "<main-block>"],

            ["<declaration-list>", "->", "<declaration>"],
            ["<declaration-list>", "->", "<declaration>", "<declaration-list>"],
            ["<declaration>", "->", "VAR", "<declaration-block-list>", "AS", "<data-type>", "\n"],
            ["<declaration-block-list>", "->", "<declaration-block>"],
            ["<declaration-block-list>", "->", "<declaration-block>", ",", "<declaration-block-list>"],
            ["<declaration-block>", "->", "ID", "=", "<assignment>"],
            ["<declaration-block>", "->", "ID"],
            ["<data-type>", "->", "INT"],
            ["<data-type>", "->", "CHAR"],
            ["<data-type>", "->", "BOOL"],
            ["<data-type>", "->", "FLOAT"],
            ["<main-block>", "->", "START", "\n", "<executable-statement-list>", "STOP"],
            ["<main-block>", "->", "START", "\n", "<executable-statement-list>", "STOP", "\n"],
            ["<executable-statement-list>", "->", "<executable-statement>", "\n"],
            ["<executable-statement-list>", "->", "<executable-statement>", "\n", "<executable-statement-list>"],
            ["<executable-statement>", "->", "ID", "=", "<assignment>"],
            ["<executable-statement>", "->", "<output>"],
            ["<executable-statement>", "->", "<input>"],
            ["<assignment>", "->", "ID", "=", "<assignment>"],
            ["<assignment>", "->", "<or-expression>"],

            ["<or-expression>", "->", "<or-expression>", "OR", "<and-expression>"],
            ["<or-expression>", "->", "<and-expression>"],

            ["<and-expression>", "->", "<and-expression>", "AND", "<equality-expression>"],
            ["<and-expression>", "->", "<equality-expression>"],

            ["<equality-expression>", "->", "<equality-expression>", "<equality-operator>", "<relational-expression>"],
            ["<equality-expression>", "->", "<relational-expression>"],
            ["<equality-operator>", "->", "=="],
            ["<equality-operator>", "->", "<>"],

            ["<relational-expression>", "->", "<relational-expression>", "<relational-operator>", "<additive-expression>"],
            ["<relational-expression>", "->", "<additive-expression>"],
            ["<relational-operator>", "->", ">"],
            ["<relational-operator>", "->", "<"],
            ["<relational-operator>", "->", ">="],
            ["<relational-operator>", "->", "<="],

            ["<additive-expression>", "->", "<additive-expression>", "<additive-operator>", "<multiplicative-expression>"],
            ["<additive-expression>", "->", "<multiplicative-expression>"],
            ["<additive-operator>", "->", "+"],
            ["<additive-operator>", "->", "-"],
            ["<additive-operator>", "->", "&"],

            ["<multiplicative-expression>", "->", "<multiplicative-expression>", "<multiplicative-operator>", "<unary-expression>"],
            ["<multiplicative-expression>", "->", "<unary-expression>"],
            ["<multiplicative-operator>", "->", "*"],
            ["<multiplicative-operator>", "->", "/"],
            ["<multiplicative-operator>", "->", "%"],

            ["<unary-expression>", "->", "<unary-operator>", "<unary-expression>"],
            ["<unary-expression>", "->", "<parenthesis-expression>"],
            ["<unary-operator>", "->", "+"],
            ["<unary-operator>", "->", "-"],
            ["<unary-operator>", "->", "NOT"],

            ["<parenthesis-expression>", "->", "(", "<or-expression>", ")"],
            ["<parenthesis-expression>", "->", "ID"],
            ["<parenthesis-expression>", "->", "CLIT"],
            ["<parenthesis-expression>", "->", "ILIT"],
            ["<parenthesis-expression>", "->", "FLIT"],
            ["<parenthesis-expression>", "->", "BLIT"],
            ["<parenthesis-expression>", "->", "SLIT"],

            ["<output>", "->", "OUTPUT:", "<or-expression>"],
            ["<input>", "->", "INPUT:", "<id-list>"],
            ["<id-list>", "->", "ID"],
            ["<id-list>", "->", "<id-list>", ",", "ID"]
        ]
