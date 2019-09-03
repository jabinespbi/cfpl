import re
from queue import Queue

from compiler.lexical.lexical import Lexical
from compiler.semantics.grammar import Grammar
from compiler.semantics.state import State
from compiler.utils import Utils


class Yacc:
    """Given rules, this class will create a dictionary which is a parser"""

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

        # queue of non terminal symbols
        queue = Queue()
        # create first state
        state = State()
        # add rule to the state <CFPL>' -> . <CFPL>$, enqueue "<CFPL>" to rules_queue
        cfpl_dash = [grammar[0][0] + "'", "->", ".", grammar[0][0]]
        state.rules.append(cfpl_dash)
        queue.put(grammar[0][0])

        # for every non terminal symbol in queue,
        while queue.empty() is False:
            non_terminal = queue.get()

            # get all the productions of that non_terminal
            productions = Grammar.find_rule(non_terminal, grammar)

            # add dot in the beginning for all the production
            for i in range(len(productions)):
                productions[i].insert(2, ".")

                # if it does not exist
                if Utils.contains_string_array(productions[i], state.rules) is False:
                    # add it to the state.rules
                    state.rules.append(productions[i])

                    # get the symbol following the dot
                    symbol_followed_by_dot = productions[i][3]

                    # if the symbol is a non terminal
                    if re.compile(r'\A<.*>\Z').match(symbol_followed_by_dot):
                        # if the symbol is not already in the queue, add it to queue
                        queue.put(symbol_followed_by_dot)

        for rule in state.rules:
            print(rule)

        # while the transitions to be expanded queue is not empty
            # for rule in state.rules
                # push all the symbol followed by dot to transition_queue with no duplicates
                # for all the symbol in transition_queue
                    # create a new state

                    # the first rule of the new state is all the
                    # rules from current state (state0) where the dot is after the symbol

                    # process all the non terminal symbol for the new state

                    # create a transition from symbol,
                    # if the new state does not exist in the list of state of the parser
                        # add the new state to the list of state of the parser
                        # set the state of the transition to the new state
                    # else
                        # set the state of the transition to the existing state
                        # add the transition to the transitions to be expanded queue

                    # add the transition to the current state (state0)

