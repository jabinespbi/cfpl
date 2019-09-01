import os


class State2:
    """This class follows the state pattern. This is the state part."""

    def go_next(self, lexical):
        if lexical.curr_index >= len(lexical.lexemes):
            raise EOFError("Found no token until the end of lexemes!")

        if lexical.lexemes[lexical.curr_index] == '\n':
            lexical.curr_state = lexical.state1
            lexical.curr_index += 1
            return None
        else:
            lexical.curr_state = lexical.state2
            lexical.curr_index += 1
            return None

