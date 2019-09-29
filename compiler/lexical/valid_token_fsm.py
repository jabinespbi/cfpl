class ValidTokenFSM:
    @staticmethod
    def is_token(possible_token):
        return ValidTokenFSM.is_operators(possible_token) or \
               ValidTokenFSM.is_reserved(possible_token) or \
               ValidTokenFSM.is_id(possible_token) or \
               ValidTokenFSM.is_bool(possible_token) or \
               ValidTokenFSM.is_int(possible_token) or \
               ValidTokenFSM.is_float(possible_token) or \
               ValidTokenFSM.is_string(possible_token) or \
               ValidTokenFSM.is_char(possible_token)

    @staticmethod
    def is_char_valid(char):
        valid_char = '()*/%+-><=&,A-Za-z$_"\'0-9.]'
        return char in valid_char

    @staticmethod
    def is_operators(possible_token):
        reserved = ['(', ')', '*', '/', '%', '+', '-', '>', '<', '=', '&', ',',
                    '>=', '<=', '==', '<>']

        for keyword in reserved:
            if possible_token == keyword:
                return True

        return False

    @staticmethod
    def is_reserved(possible_token):
        reserved = ['INT', 'CHAR', 'BOOL', 'FLOAT', 'AND', 'OR', 'NOT', 'START', 'STOP', 'VAR', 'AS', 'OUTPUT:',
                    'INPUT:', 'IF', 'ELSE', 'WHILE']

        for keyword in reserved:
            if possible_token == keyword:
                return True

        return False

    @staticmethod
    def is_id(possible_token):
        first_char = '$_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        following_char = '$_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

        if possible_token[0] not in first_char:
            return False

        for c in range(1, len(possible_token)):
            if c not in following_char:
                return False

        return True

    @staticmethod
    def is_bool(possible_token):
        if possible_token == "TRUE" or \
                possible_token == "FALSE":
            return True

        return False

    @staticmethod
    def is_int(possible_token):
        valid_char = '0123456789'

        for c in possible_token:
            if c not in valid_char:
                return False

        return True

    @staticmethod
    def is_float(possible_token):
        valid_char = '0123456789'

        char_num = 0
        for c in possible_token:
            if c == '.':
                char_num += 1
                break

            char_num += 1
            if c not in valid_char:
                return False

        if char_num >= len(possible_token):
            return False

        char_num += 1
        for c in range(char_num, len(possible_token)):
            if c not in valid_char:
                return False

        return True

    @staticmethod
    def is_string(possible_token):
        if len(possible_token) < 2:
            return False
        if possible_token[0] != '"':
            return False
        if possible_token[len(possible_token) - 1] != '"':
            return False

        return True

    @staticmethod
    def is_char(possible_token):
        if len(possible_token) < 2:
            return False
        if possible_token[0] != "'":
            return False
        if possible_token[len(possible_token) - 1] != "'":
            return False

        return True





