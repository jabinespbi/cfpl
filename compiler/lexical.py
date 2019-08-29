import re

class Lexical:
    """The lexical analyzer for the language. The dfa is a dictionary with partly regex for
    identifying valid tokens."""

    token_regex = r'[()*/%+\-><=]|>=|<=|==|<>|VAR|AS|INT|CHAR|BOOL|FLOAT|AND|OR|NOT|START|STOP|&|,|[$_a-z][$_a-zA-Z0-9]*|\".*\"'

    curr_state = 0
    dfa_table = {
        0: {  # from state 0
            '\n': [0, 0],  # '\n' is the input, [a, b] a = go to this state, b = if 1, a token is found
            '*': [1, 0],
            ' ': [2, 0],
            'token': [3, 1],
        },
        1: {
            '\n': [0, 0],
            '!\n': [1, 0],
        },
        2: {
            '\n': [0, 0],
            '*': [1, 0],
            ' ': [2, 0],
            'token': [3, 1],
        },
        3: {
            ' ': [3, 0],
            'token': [3, 1],
            '\n': [0, 1],
        }
    }

    lex_ptr = 0  # current index of the lexical analyzer
    start = 0  # index for the start of the token
    end = 0  # index for end of token (exclusive)

    def __init__(self, lexemes):
        self.lexemes = lexemes

    def next(self):
        self.start = self.lex_ptr  # start with the current index
        self.end = self.lex_ptr  # end with the current index

        while self.start < len(self.lexemes):
            try:
                output = self.dfa_table[self.curr_state][self.lexemes[self.start]]
                if output[1] == 1:
                    return self.lexemes[self.lex_ptr]

                self.start += 1
                self.curr_state = output[0]
            except KeyError:
                if self.curr_state == 0 or self.curr_state == 2 or self.curr_state == 3:
                    # 'regex for token'
                    re
                elif self.curr_state == 1:
                    'regex for !\n'
                else:
                    print('Something went wrong!')

    def token_regex(self):
        lex_ptr = 0
        end = lex_ptr + 1

        # while end < len(line):
        #     possible_token = line[lex_ptr:end]
        #     matchObj = re.search(token_regex, possible_token)
        #
        #     if matchObj:
        #         string_matched1 = matchObj.group()
        #
        #         # try matching the next token (longest rule matching)
        #         possible_longer_token = line[lex_ptr:end + 1]
        #         matchObj = re.search(token_regex, possible_longer_token)
        #
        #         if matchObj:
        #             string_matched2 = matchObj.group()
        #
        #             print(string_matched1, " ", string_matched2)
        #             if string_matched1 == string_matched2:
        #                 lex_ptr = end + 1
        #                 print(string_matched1)
        #                 break
        #             else:
        #                 end += 1
        #
        #     end += 1
