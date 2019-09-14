from queue import Queue

from compiler.lexical.lexical import Lexical
from compiler.semantics.grammar import Grammar
from compiler.semantics.state import State
from compiler.semantics.transition import Transition
from compiler.utils import Utils


class Yacc:
    """Given the grammar, this class will create an slr(1) parsing table."""

    def __init__(self, grammar, source_code):
        """grammar format: an array of rules
            the first rule is the starting state or starting rule
            [
                ["E", "->", "E", "+", "F"],
                ["F", "->", "+", "G"],
                ["G", "->", "id"]
            ]
        """
        self.lexical = Lexical(source_code)
        self.grammar = grammar
        self.parser_states = []

    def create_parser(self):
        # create first state
        state0 = State()
        # add rule to the state <CFPL>' -> . <CFPL>$
        dash = [self.grammar[0][0] + "'", "->", ".", self.grammar[0][0]]
        state0.rules.append(dash)
        self.add_rules_with_nonterminal_followed_by_dot(state0)

        self.parser_states.append(state0)

        unexpanded_states_queue = Queue()
        unexpanded_states_queue.put(state0)

        while unexpanded_states_queue.empty() is False:
            state = unexpanded_states_queue.get()
            transition_inputs_queue = Queue()
            for transition_input in self.get_transition_inputs(state):
                transition_inputs_queue.put(transition_input)

            # while transition_inputs_queue is not empty
            while transition_inputs_queue.empty() is False:
                new_state = State()
                transition_input = transition_inputs_queue.get()

                for rule in state.rules:
                    symbol = Utils.get_symbol_followed_by_dot(rule)
                    if symbol == transition_input:
                        rule_copy = rule.copy()

                        index = rule_copy.index('.')
                        rule_copy.pop(index)
                        rule_copy.insert(index + 1, '.')

                        new_state.rules.append(rule_copy)

                self.add_rules_with_nonterminal_followed_by_dot(new_state)
                transition = Transition()

                # if new_state doesn't exist
                similar_state = Utils.get_same_state_in_list(self.parser_states, new_state)
                if similar_state is None:
                    transition.state = new_state
                    self.parser_states.append(new_state)
                    unexpanded_states_queue.put(new_state)
                else:
                    transition.state = similar_state
                transition.transition_input = transition_input

                state.transitions.append(transition)

    def add_rules_with_nonterminal_followed_by_dot(self, state):
        """given state with initial rules, add rules to the state for all the current rules
        that has a production of dot followed by a non terminal"""
        # list of non terminal symbols
        unprocessed_rules = Queue()
        for rule in state.rules:
            unprocessed_rules.put(rule)

        # for every non terminal symbol in queue,
        while unprocessed_rules.empty() is False:
            rule = unprocessed_rules.get()

            # if rule's dot followed by a non terminal
            nonterminal = Utils.get_nonterminal_followed_by_dot(rule)
            if nonterminal is None:
                continue

            # get all the rules of that non_terminal
            rules_of_nonterminal = Grammar.find_rule_and_deep_copy(nonterminal, self.grammar)

            # add dot in the beginning for all the production
            for i in range(len(rules_of_nonterminal)):
                rules_of_nonterminal[i].insert(2, ".")

                # if rules_of_nonterminal does not exist in state.rules
                if rules_of_nonterminal[i] not in state.rules:
                    # add it to the state.rules and unprocessed_rules
                    state.rules.append(rules_of_nonterminal[i])
                    unprocessed_rules.put(rules_of_nonterminal[i])

    def get_transition_inputs(self, state):
        # add all symbols (terminal and nonterminal) to transition_inputs_queue
        transition_inputs = []
        for rule in state.rules:
            symbol = Utils.get_symbol_followed_by_dot(rule)
            if symbol is not None and symbol not in transition_inputs:
                transition_inputs.append(symbol)

        return transition_inputs

