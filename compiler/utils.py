import re
from queue import Queue

from compiler.lexical.valid_token_fsm import ValidTokenFSM
from compiler.symbols.symbol_table import SymbolTable
from compiler.unexpected_error import UnexpectedError


class Utils:

    @staticmethod
    def get_nonterminal_followed_by_dot(rule):
        """returns an index of the array where the string_to_look_up is located"""
        try:
            index = rule.index('.')
            if index + 1 < len(rule):
                symbol = rule[index + 1]

                # if the symbol is a non terminal
                if re.compile(r'\A<.*>\Z').match(symbol):
                    return symbol
        except ValueError:
            print("No '.' in the rule. Hmmm...")

        return None

    @staticmethod
    def get_symbol_followed_by_dot(rule):
        """returns an index of the array where the string_to_look_up is located"""
        try:
            index = rule.index('.')
            if index + 1 < len(rule):
                return rule[index + 1]
        except ValueError:
            print("No '.' in the rule. Hmmm...")

        return None

    @staticmethod
    def get_same_state_in_list(state_list, state_to_find):
        """get state that has the same rules with state_to_find in state_list"""
        for state in state_list:
            found = Utils.are_states_rules_similar(state, state_to_find)
            if found is True:
                return state

        return None

    @staticmethod
    def are_states_rules_similar(state1, state2):
        """checks if the rules of two states is the same"""
        state1_rules_len = len(state1.rules)
        state2_rules_len = len(state2.rules)

        if state1_rules_len != state2_rules_len:
            return False

        state2_indexes_done = []  # keep indexes of state2 that are done matching with state1
        for state1_index in range(state1_rules_len):

            found = False
            for state2_index in range(state2_rules_len):
                if state2_index in state2_indexes_done:
                    continue

                if state1.rules[state1_index] == state2.rules[state2_index]:
                    found = True
                    state2_indexes_done.append(state2_index)
                    break

            if found is False:
                return False

        return True

    @staticmethod
    def are_rules_similar(rule1, rule2):
        """checks if two rules are similar"""
        rule1_len = len(rule1)
        rule2_len = len(rule2)

        if rule1_len != rule2_len:
            return False

        for x in range(rule1_len):
            if rule1[x] != rule2[x]:
                return False

        return True

    @staticmethod
    def follow(nonterminal, grammar):
        """return a list of follows of symbol.
        the first rule is the start rule of the grammar.
        the follow of first rule is EoI (End of Input)"""
        follows = []
        first_nonterminal = grammar[0][0]

        done = [nonterminal]
        queue = Queue()
        queue.put(nonterminal)

        while queue.empty() is False:
            nonterminal = queue.get()

            if nonterminal is first_nonterminal and "EoI" not in follows:
                follows.append("EoI")

            for rule in grammar:
                follows_rule = Utils.follow_rule(rule, nonterminal, grammar)
                if follows_rule['follow_rule'] and rule[0] not in done:
                    queue.put(rule[0])
                    done.append(rule[0])

                for follow_rule in follows_rule['follows']:
                    if follow_rule not in follows:
                        follows.append(follow_rule)

        return follows

    @staticmethod
    def follow_rule(rule, nonterminal, grammar):
        return_value = {
            'follows': [],
            'follow_rule': False  # true if needs to continue following lhs of the rule (follow(lhs)) because
            # follow(nonterminal) hits the end of the rule
        }

        for x in range(2, len(rule)):
            if rule[x] is nonterminal:
                if x + 1 < len(rule):
                    for y in range(x + 1, len(rule)):
                        if Utils.is_nonterminal(rule[y]):
                            firsts = Utils.first(rule[y], grammar)
                            for first in firsts:
                                if first not in return_value['follows']:
                                    return_value['follows'].append(first)
                            if Utils.contains_empty_production(rule[y], grammar) is False:
                                return_value['follow_rule'] = False
                                break
                            elif y is len(rule) - 1:
                                return_value['follow_rule'] = True
                        elif rule[y] is not "":
                            if rule[y] not in return_value['follows']:
                                return_value['follows'].append(rule[y])
                                return_value['follow_rule'] = False
                            break
                        else:
                            raise UnexpectedError("Unexpected empty production!")
                else:
                    return_value['follow_rule'] = True

        return return_value

    @staticmethod
    def first(nonterminal, grammar):
        """return a list of first of nonterminal"""
        firsts_of_nonterminal = []
        done = [nonterminal]  # keeps the finished nonterminal

        queue = Queue()
        queue.put(nonterminal)
        while queue.empty() is False:
            nonterminal = queue.get()
            rules = Utils.get_rules_by_lhs(nonterminal, grammar)
            for rule in rules:
                for x in range(2, len(rule)):  # right hand side begins after '->'
                    if re.compile(r'\A<.*>\Z').match(rule[x]):
                        if rule[x] not in done:
                            queue.put(rule[x])
                            done.append(rule[x])
                        # check if rule[x] has empty production
                        if Utils.contains_empty_production(rule[x], grammar):
                            continue
                        else:
                            break
                    elif rule[x] is not "":
                        firsts_of_nonterminal.append(rule[x])
                        break

        return firsts_of_nonterminal

    @staticmethod
    def get_rules_by_lhs(nonterminal, grammar):
        """return a list of rules that has lhs equal to symbol"""
        rules = []
        for rule in grammar:
            if rule[0] is nonterminal:
                rules.append(rule)

        return rules

    @staticmethod
    def contains_empty_production(nonterminal, grammar):
        """return true if nonterminal in the grammar produces empty production"""
        rules = Utils.get_rules_by_lhs(nonterminal, grammar)
        for rule in rules:
            if len(rule) is not 3:  # empty production is in format of ['<nonterminal>', "->", ""]
                continue
            else:
                if rule[2] is "":
                    return True

        return False

    @staticmethod
    def is_nonterminal(symbol):
        return re.compile(r'\A<.*>\Z').match(symbol)

    @staticmethod
    def is_string_match_regex(string, regex):
        return re.compile(regex).match(string)

    @staticmethod
    def get_all_symbols(grammar):
        symbols = []
        for rule in grammar:
            for symbol in range(2, len(rule)):
                if rule[symbol] is not "" and rule[symbol] not in symbols:
                    symbols.append(rule[symbol])

        return symbols

    @staticmethod
    def get_grammar_symbol(token):
        if ValidTokenFSM.is_reserved(token):
            return None
        elif ValidTokenFSM.is_id(token):
            return "ID"
        elif ValidTokenFSM.is_bool(token):
            return "BLIT"
        elif ValidTokenFSM.is_int(token):
            return "ILIT"
        elif ValidTokenFSM.is_float(token):
            return "FLIT"
        elif ValidTokenFSM.is_string(token):
            return "SLIT"
        elif ValidTokenFSM.is_char(token):
            return "CLIT"
        else:
            return None

    @staticmethod
    def add_symbol_to_symbol_table(token_indexes_found, lexemes):
        symbol = lexemes[token_indexes_found[0]: token_indexes_found[1]]
        grammar_symbol = Utils.get_grammar_symbol(symbol)
        SymbolTable.getInstance().unknown_tokens[token_indexes_found[0]] = {
            "uid": token_indexes_found[0],
            "token": symbol,
            "grammar_symbol": grammar_symbol,
            "type": None,  # used in semantics
            "value": None  # used in runtime
        }

    @staticmethod
    def grammar_type_to_data_type(grammar_type):
        if grammar_type == "CLIT":
            return "CHAR"
        elif grammar_type == "ILIT":
            return "INT"
        elif grammar_type == "FLIT":
            return "FLOAT"
            return "FLOAT"
        elif grammar_type == "BLIT":
            return "BOOL"
        else:
            raise Exception("Unexpected argument ", grammar_type, "!")

    @staticmethod
    def data_type_to_grammar_type(grammar_type):
        if grammar_type == "CHAR":
            return "CLIT"
        elif grammar_type == "INT":
            return "ILIT"
        elif grammar_type == "FLOAT":
            return "FLIT"
        elif grammar_type == "BOOL":
            return "BLIT"
        elif grammar_type == "STRING":
            return "SLIT"
        else:
            raise Exception("Unexpected argument ", grammar_type, "!")

    @staticmethod
    def near(lexemes, lex_ptr):
        end_index = len(lexemes)
        if lex_ptr + 10 < end_index:
            end_index = lex_ptr + 10
        near_message = lexemes[lex_ptr: end_index]
        if "\n" in near_message:
            index_of_n = near_message.index("\n")
            return near_message[0: index_of_n]

        return near_message

    @staticmethod
    def line_number(lexemes, lex_ptr):
        return lexemes[0: lex_ptr].count('\n') + 1

    @staticmethod
    def is_id_of_type(operand, data_type):
        """operand is either dict which is an ID or a literal.
        data_type should be the grammar data type (e.g. INT, CHAR)"""
        if type(operand) is not dict:
            raise Exception("Argument should be a dictionary!")

        id_data_type = SymbolTable.getInstance().symbol_table[operand['token']]['type']
        if operand['grammar_symbol'] != "ID":
            raise Exception("Argument should be an ID!")

        return id_data_type == data_type

    @staticmethod
    def is_literal_of_type(literal, data_type):
        if type(literal) is not dict:
            raise Exception("Argument should be a dictionary!")

        return literal['grammar_symbol'] == Utils.data_type_to_grammar_type(data_type)

    @staticmethod
    def is_declared(variable):
        """variable should be a dictionary"""
        if type(variable) is not dict:
            raise Exception("Argument should be a dictionary!")

        return variable['token'] in SymbolTable.getInstance().symbol_table

    @staticmethod
    def is_id(variable):
        """variable should be a dictionary"""
        if type(variable) is not dict:
            raise Exception("Argument should be a dictionary!")

        return variable['grammar_symbol'] == "ID"

    @staticmethod
    def is_error(variable):
        """variable should be a dictionary"""
        if type(variable) is not dict:
            raise Exception("Argument should be a dictionary!")

        return variable['grammar_symbol'] == "ERROR"

    @staticmethod
    def is_literal(variable):
        """variable should be a dictionary"""
        if type(variable) is not dict:
            raise Exception("Argument should be a dictionary!")

        return variable['grammar_symbol'] == "CLIT" or \
               variable['grammar_symbol'] == "ILIT" or \
               variable['grammar_symbol'] == "FLIT" or \
               variable['grammar_symbol'] == "BLIT" or \
               variable['grammar_symbol'] == "SLIT"
