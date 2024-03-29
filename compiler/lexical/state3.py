from compiler.lexical.valid_token import ValidToken
from compiler.utils import Utils


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
            token_indexes_found = [token_index, token_index + 1]
            Utils.add_symbol_to_symbol_table(token_indexes_found, lexical.lexemes)
            return token_indexes_found
        elif curr_char == ' ' or curr_char == '\t':
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

