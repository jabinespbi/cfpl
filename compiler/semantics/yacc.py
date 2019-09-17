from queue import Queue

from compiler.lexical.lexical import Lexical
from compiler.parsing_table_error import ParsingTableError
from compiler.semantics.action import Action
from compiler.semantics.action_type import ActionType
from compiler.semantics.grammar import Grammar
from compiler.semantics.state import State
from compiler.semantics.transition import Transition
from compiler.symbols.symbol_table import SymbolTable
from compiler.tree import Tree
from compiler.utils import Utils


class Yacc:
    """Given the grammar, this class will create an slr(1) parsing table."""

    def __init__(self, grammar, source_code):
        """grammar format: an array of rules
            the first rule is the starting state or starting rule
            [
                ["E", "->", "E", "+", "F"],
                ["F", "->", "+", "G"],
                ["G", "->", "id"],
                ["G"], "->", ""]            -> means that G can be empty, this is what this yacc
                                                assumes with empty production
            ]
        """
        self.lexical = Lexical(source_code)
        self.grammar = grammar
        self.parser_states = []
        self.slr1 = {}
        self.parse_tree = None

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

    def create_parsing_table(self):
        """creates slr(1) parsing table after calling create_parser() which creates the finite state diagram"""
        symbols = Utils.get_all_symbols(self.grammar)
        symbols.append("EoI")
        for x in range(len(self.parser_states)):
            self.slr1[x] = {}
            for symbol in symbols:
                self.slr1[x][symbol] = None

        for x in range(len(self.parser_states)):
            state = self.parser_states[x]
            for rule in state.rules:
                if rule[len(rule) - 1] == '.':  # if reduce state
                    if rule[0][len(rule[0]) - 1] == "'":    # if accept state
                        action = Action()
                        action.type = ActionType.ACCEPT
                        self.slr1[x]["EoI"] = action
                    else:
                        follows = Utils.follow(rule[0], self.grammar)
                        action = Action()
                        action.type = ActionType.REDUCE
                        action.reduce_rule = rule.copy()
                        action.reduce_rule.remove('.')
                        for follow in follows:
                            if self.slr1[x][follow] is not None:
                                conflict = self.slr1[x][follow].type
                                message = "Found confict : reduce - " + conflict.name + " at state " + str(x) + " on input '" + follow + "'"
                                raise ParsingTableError(message)

                            self.slr1[x][follow] = action

            for transition in state.transitions:
                if Utils.is_nonterminal(transition.transition_input):
                    action = Action()
                    action.type = ActionType.GOTO
                    action.next_state = self.parser_states.index(transition.state)
                    self.slr1[x][transition.transition_input] = action
                else:
                    action = Action()
                    action.type = ActionType.SHIFT
                    action.next_state = self.parser_states.index(transition.state)
                    if self.slr1[x][transition.transition_input] is not None:
                        conflict = self.slr1[x][transition.transition_input].type
                        message = "Found confict : shift - " + conflict.name + " at state " + str(x) + " on input " + transition.transition_input
                        raise ParsingTableError(message)

                    self.slr1[x][transition.transition_input] = action

    def create_parse_tree(self):
        """Creates the parse tree using the slr1 parsing table"""
        stack = ["EoS", 0]
        try:
            while True:
                token_indexes = self.lexical.next()
                symbol = SymbolTable.getInstance().unknown_tokens[token_indexes[0]]
                grammar_symbol = symbol.token

                if symbol.grammar_symbol is not None:
                    grammar_symbol = symbol.grammar_symbol
                action = self.slr1[stack[-1]][grammar_symbol]

                if action.type is ActionType.SHIFT:
                    node = Tree()
                    node.root = symbol
                    stack.append(node)
                    stack.append(action.next_state)
                elif action.type is ActionType.GOTO:
                    raise Exception("Unexpected action type: GOTO! GOTO should only be after reduce action!")
                elif action.type is ActionType.REDUCE:
                    parent = Tree()
                    reduce_rule = action.reduce_rule
                    parent.root = reduce_rule[0]
                    rhs_length = len(reduce_rule) - 2

                    for x in range(rhs_length):
                        stack.pop()
                        child = stack.pop()
                        parent.children.append(child)

                    action = self.slr1[stack[-1]][reduce_rule[0]]
                    if action.type is not ActionType.GOTO:
                        raise Exception("Unexpected action type: " + action.type.name + "! Should be GOTO action!")

                    stack.append(parent)
                    stack.append(action.next_state)
                elif action.type is ActionType.ACCEPT:
                    self.parse_tree = stack[-1]
                    print("Syntax analysis is complete!")
                    return
        except EOFError:
            print("Found the end of input")

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


