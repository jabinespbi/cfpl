import re
from queue import Queue

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
        """return a list of follows of symbol."""
        follows = []

        done = [nonterminal]
        queue = Queue()
        queue.put(nonterminal)

        while queue.empty() is False:
            nonterminal = queue.get()

            for rule in grammar:
                Utils.follow_rule(rule, nonterminal, grammar)

    @staticmethod
    def follow_rule(rule, nonterminal, grammar):
        return_value = {
            'follows': [],
            'follow_rule': True         # true if needs to continue following lhs of the rule (follow(lhs)) because
                                        # follow(nonterminal) hits the end of the rule
        }

        for x in range(2, len(rule)):
            if rule[x] is nonterminal:
                if x + 1 <= len(rule):
                    for y in range(x + 1, len(rule)):
                        if Utils.is_nonterminal(rule[y]):
                            firsts = Utils.first(nonterminal, grammar)
                            for first in firsts:
                                if first not in return_value['follows']:
                                    return_value['follows'].append(first)
                            if Utils.contains_empty_production(rule[y], grammar) is False:
                                return_value['follow_rule'] = False
                                break
                        elif rule[y] is not "":
                            if rule[y] not in return_value['follows']:
                                return_value['follows'].append(rule[y])
                                return_value['follow_rule'] = False
                            break
                        else:
                            raise UnexpectedError("Unexpected empty production!")

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