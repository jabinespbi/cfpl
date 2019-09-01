from compiler.lexical.state1 import State1
from compiler.lexical.state2 import State2
from compiler.lexical.state3 import State3


class Lexical:
    """The lexical analyzer for the language in which the dfa is not implemented completely by a table
    just like lex tool. Some parts are regex.

    This class follows the state pattern in which this is the context part."""

    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.curr_index = 0  # the current index of the lexemes
        self.state1 = State1()
        self.state2 = State2()
        self.state3 = State3()
        self.curr_state = self.state1  # the current state of the lexical

    def next(self):
        token_indexes = None
        while token_indexes is None:
            token_indexes = self.curr_state.go_next(self)

            if token_indexes:
                return token_indexes

    def get_all_tokens(self):
        tokens = []

        while True:
            try:
                token_indexes = self.next()
                tokens.append(self.lexemes[token_indexes[0]: token_indexes[1]])
            except EOFError:
                break

        return tokens
