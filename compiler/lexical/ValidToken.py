import re


class ValidToken:
    token_regex = r'\A(' \
                  r'[\(\)*/%+\-><=&,]|' \
                  r'>=|<=|==|<>|' \
                  r'INT|CHAR|BOOL|FLOAT|AND|OR|NOT|' \
                  r'START|STOP|VAR|AS|OUTPUT:|INPUT:|' \
                  r'[$_a-zA-Z][$_a-zA-Z0-9]*|' \
                  r'[0-9]*|' \
                  r'\".*\"|' \
                  r'\'.\'|' \
                  r')\Z'

    def check(self, lexemes, curr_ptr):
        # lexemes should start a character of the token
        # because the part that will take away the unnecessary characters is done
        # before it reaches to invoke this action

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
                    return token_indexes_found

            end += 1

        return token_indexes_found
