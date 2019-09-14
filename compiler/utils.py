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

        state2_indexes_done = []    # keep indexes of state2 that are done matching with state1
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

