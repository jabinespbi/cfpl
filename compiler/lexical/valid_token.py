import re

from compiler.error_handler.error_handler import ErrorHandler
from compiler.utils import Utils


class ValidToken:
    token_regex = r'\A(' \
                  r'[\(\)*/%+\-><=&,]|' \
                  r'>=|<=|==|<>|' \
                  r'INT|CHAR|BOOL|FLOAT|AND|OR|NOT|' \
                  r'START|STOP|VAR|AS|OUTPUT:|INPUT:|' \
                  r'[$_a-zA-Z][$_a-zA-Z0-9]*|' \
                  r'\"((TRUE)|(FALSE))\"|' \
                  r'[0-9]+|' \
                  r'[0-9]*\.[0-9]+|' \
                  r'\".*\"|' \
                  r'\'.\'' \
                  r') ?\Z'

    first_char_valid = r'\A(' \
                       r'[\(\)*/%+\-><=&,A-Za-z$_\"\'0-9.]|' \
                       r')\Z'

    def check(self, lexemes, curr_ptr):
        """ lexemes should start a character of the token
        because the part that will take away the unnecessary characters is done
        before it reaches to invoke this action.
        add contents to the symbol table"""

        lex_ptr = curr_ptr
        end = lex_ptr + 1

        while True:
            first_character_of_token = lexemes[lex_ptr:end]
            if first_character_of_token == " ":
                lex_ptr = end
                end = end + 1
                continue

            if re.match(self.first_char_valid, first_character_of_token) is None:
                msg = "Illegal character: " + first_character_of_token + " near " + Utils.near(lexemes, lex_ptr)
                ErrorHandler.getInstance().lex_errors.append(msg)
                lex_ptr = end
                end = end + 1
                continue
            else:
                break

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
                    if possible_token[len(possible_token) - 1] == " ":
                        token_indexes_found[1] = token_indexes_found[1] - 1
                    Utils.add_symbol_to_symbol_table(token_indexes_found, lexemes)
                    return token_indexes_found

            end += 1

        if token_indexes_found is not None:
            token = lexemes[token_indexes_found[0]: token_indexes_found[1]]
            if token[len(token) - 1] == " ":
                token_indexes_found[1] = token_indexes_found[1] - 1
            Utils.add_symbol_to_symbol_table(token_indexes_found, lexemes)
        return token_indexes_found
