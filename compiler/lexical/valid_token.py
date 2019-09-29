import re

from compiler.error_handler.error_handler import ErrorHandler
from compiler.lexical.valid_token_fsm import ValidTokenFSM
from compiler.utils import Utils


# TODO: 'asdfasdf' should be a valid character
# TODO string "asdfasdfasdf["]" should be considered as valid and one string
class ValidToken:

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

            if ValidTokenFSM.is_char_valid(first_character_of_token) is False:
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
            matchObj = ValidTokenFSM.is_token(possible_token)

            if matchObj:
                token_indexes_found = [lex_ptr, end]
                # try matching the next token (longest rule matching)
                possible_longer_token = lexemes[lex_ptr:end + 1]
                matchObj = ValidTokenFSM.is_token(possible_longer_token)

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
