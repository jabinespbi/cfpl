import re


# TODO: VAR x, w_23='w' AS CHAR(not included uninitialized and initalized in the same assignment statement
from compiler.symbols.symbol_table import SymbolTable
from compiler.utils import Utils


class ValidToken:
    token_regex = r'\A(' \
                  r'[\(\)*/%+\-><=&,]|' \
                  r'>=|<=|==|<>|' \
                  r'INT|CHAR|BOOL|FLOAT|AND|OR|NOT|' \
                  r'START|STOP|VAR|AS|OUTPUT:|INPUT:|' \
                  r'[$_a-zA-Z][$_a-zA-Z0-9]*|' \
                  r'\"(TRUE)|(FALSE)\"|' \
                  r'[0-9]+|' \
                  r'[0-9]*\.[0-9]+|' \
                  r'\".*\"|' \
                  r'\'.\'|' \
                  r')\Z'

    def check(self, lexemes, curr_ptr):
        """ lexemes should start a character of the token
        because the part that will take away the unnecessary characters is done
        before it reaches to invoke this action.
        add contents to the symbol table"""

        lex_ptr = curr_ptr
        end = lex_ptr + 1

        token_indexes_found = None
        while end <= len(lexemes):

            possible_token = lexemes[lex_ptr:end]
            matchObj = re.match(self.token_regex, possible_token)

            if matchObj:
                token_indexes_found = [lex_ptr, end]
                # try matching the next token (longest rule matching)
                possible_longer_token = lexemes[lex_ptr:end + 1]
                matchObj = re.match(self.token_regex, possible_longer_token)

                if matchObj is None:
                    Utils.add_symbol_to_symbol_table(token_indexes_found, lexemes)
                    return token_indexes_found

            end += 1

        if token_indexes_found is not None:
            Utils.add_symbol_to_symbol_table(token_indexes_found, lexemes)
        return token_indexes_found
