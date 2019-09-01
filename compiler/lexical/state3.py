import os

from compiler.lexical.ValidToken import ValidToken


class State3:
    """This class follows the state pattern. This is the state part."""

    def go_next(self, lexical):
        if lexical.curr_index >= len(lexical.lexemes):
            raise EOFError("Found no token until the end of lexemes!")

        curr_char = lexical.lexemes[lexical.curr_index]

        if curr_char == '\n':
            lexical.curr_state = lexical.state1
            token_index = lexical.curr_index
            lexical.curr_index += 1
            return [token_index, token_index + 1]
        elif curr_char == ' ':
            lexical.curr_state = lexical.state3
            lexical.curr_index += 1
            return None
        else:
            token_indexes = ValidToken().check(lexical.lexemes, lexical.curr_index)
            if token_indexes is None:
                raise EOFError("Found no token until the end of lexemes!")

            else:
                lexical.curr_state = lexical.state3
                lexical.curr_index = token_indexes[1]
                return token_indexes

