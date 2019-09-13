import re


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
    def list_contains_state(list, state_to_check):
        """checks the state_to_check if it has the same rules with any of the list.
        when iterating the list, the state from the list and the state_to_check should
        have similar rule in the same indexes for this function to return true"""
        for state in list:
            state_rules = state.rules
            for x in len(state_rules):

