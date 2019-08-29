#!/usr/bin/python
import re

line = "      abc, b, c AS INT"
token_regex = r'[()*/%+\-><=]|>=|<=|==|<>|VAR|AS|INT|CHAR|BOOL|FLOAT|AND|OR|NOT|START|STOP|&|,|[$_a-z][$_a-zA-Z0-9]*|\".*\"'

lex_ptr = 0
end = lex_ptr + 1

while end < len(line):
    possible_token = line[lex_ptr:end]
    matchObj = re.search(token_regex, possible_token)

    if matchObj:
        string_matched1 = matchObj.group()

        # try matching the next token (longest rule matching)
        possible_longer_token = line[lex_ptr:end + 1]
        matchObj = re.search(token_regex, possible_longer_token)

        if matchObj:
            string_matched2 = matchObj.group()

            print(string_matched1, " ", string_matched2)
            if string_matched1 == string_matched2:
                lex_ptr = end + 1
                print(string_matched1)
                break
            else:
                end += 1

    end += 1
