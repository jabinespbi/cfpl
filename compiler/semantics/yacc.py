import re
from queue import Queue

from compiler.lexical.lexical import Lexical
from compiler.semantics.grammar import Grammar
from compiler.semantics.state import State
from compiler.utils import Utils


class Yacc:
    """Given rules, this class will create a dictionary which is a parser"""

    def __init__(self, source_code):
        self.lexical = Lexical(source_code)

        # queue of non terminal symbols
        queue = Queue()
        # create first state
        state = State()
        # add rule to the state <CFPL>' -> . <CFPL>$, enqueue "<CFPL>" to rules_queue
        cfpl_dash = ["<CFPL>'", "->", ".", "<CFPL>"]
        state.rules.append(cfpl_dash)
        queue.put("<CFPL>")

        # for every non terminal symbol in queue,
        while queue.empty() is False:
            non_terminal = queue.get()

            # get all the productions of that non_terminal
            productions = Grammar.find_rule(non_terminal)

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

        # for all the rules in state
            #
