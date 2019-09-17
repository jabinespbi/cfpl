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
            ["<CFPL>", "->", "<DL>", "<MB>"],
            ["<CFPL>", "->", "<DL>"],
            ["<CFPL>", "->", "<MB>"],
            ["<DL>", "->", "<D>"],
            ["<DL>", "->", "<D>", "<DL>"],
            ["<D>", "->", "VAR", "<DBL>", "AS", "<DT>", "\n"],
            ["<DBL>", "->", "<DB>"],
            ["<DBL>", "->", "<DB>", ",", "<DBL>"],
            ["<DB>", "->", "<ASS>"],
            ["<DB>", "->", "ID"],
            ["<DT>", "->", "INT"],
            ["<DT>", "->", "CHAR"],
            ["<DT>", "->", "BOOL"],
            ["<DT>", "->", "FLOAT"],
            ["<MB>", "->", "START", "\n", "<ES>", "STOP"],
            ["<MB>", "->", "START", "\n", "<ES>", "STOP", "\n"],
            ["<ES>", "->", "<E>"],
            ["<ES>", "->", "<E>", "<ES>"],
            ["<E>", "->", "<ASS>"],
            ["<E>", "->", "<OUT>"],
            ["<E>", "->", "<INT>"],
            ["<ASS>", "->", "ID", "=", "<ASS>"],
            ["<ASS>", "->", "<EXP>"],
            ["<EXP>", "->", "<EXP>", "OR", "<EXPA>"],
            ["<EXP>", "->", "<EXPA>"],
            ["<EXPA>", "->", "<EXPA>", "AND", "<EXPE>"],
            ["<EXPA>", "->", "<EXPE>"],
            ["<EXPE>", "->", "<EXPE>", "<EQ>", "<EXPR>"],
            ["<EXPE>", "->", "<EXPR>"],
            ["<EQ>", "->", "=="],
            ["<EQ>", "->", "<>"],
            ["<EXPR>", "->", "<EXPR>", "<REL>", "<EXPADD>"],
            ["<EXPR>", "->", "<EXPADD>"],
            ["<REL>", "->", ">"],
            ["<REL>", "->", "<"],
            ["<REL>", "->", ">="],
            ["<REL>", "->", "<="],
            ["<EXPADD>", "->", "<EXPADD>", "<ADD>", "<EXPM>"],
            ["<EXPADD>", "->", "<EXPM>"],
            ["<ADD>", "->", "+"],
            ["<ADD>", "->", "-"],
            ["<ADD>", "->", "&"],
            ["<EXPM>", "->", "<EXPM>", "<MUL>", "<EXPU>"],
            ["<EXPM>", "->", "<EXPU>"],
            ["<MUL>", "->", "*"],
            ["<MUL>", "->", "/"],
            ["<MUL>", "->", "%"],
            ["<EXPU>", "->", "<UNA>", "<EXPU>"],
            ["<EXPU>", "->", "<EXPP>"],
            ["<UNA>", "->", "+"],
            ["<UNA>", "->", "-"],
            ["<UNA>", "->", "NOT"],
            ["<EXPP>", "->", "(", "<EXPP>", ")"],
            ["<EXPP>", "->", "ID"],
            ["<EXPP>", "->", "CLIT"],
            ["<EXPP>", "->", "ILIT"],
            ["<EXPP>", "->", "FLIT"],
            ["<EXPP>", "->", "BLIT"],
            ["<EXPP>", "->", "SLIT"],
        ]
