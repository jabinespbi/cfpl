from compiler.error_handler.error_handler import ErrorHandler
from compiler.semantics.action_type import ActionType
from compiler.symbols.symbol_table import SymbolTable
from compiler.tree import Tree
from compiler.utils import Utils


class ParseTree:
    """This is the syntax analysis part of the compiler.
    Creates the parse tree using the slr1 parsing table"""

    @staticmethod
    def create_parse_tree(lexical, slr1):
        stack = ["EoS", 0]
        try:
            token_indexes = lexical.next()
            while True:
                symbol = SymbolTable.getInstance().unknown_tokens[token_indexes[0]]
                grammar_symbol = symbol['token']

                if symbol['grammar_symbol'] is not None:
                    grammar_symbol = symbol['grammar_symbol']
                action = slr1[stack[-1]][grammar_symbol]

                if action is None:
                    msg = "A syntax error is found near " + Utils.near(lexical.lexemes, token_indexes[0])
                    ErrorHandler.getInstance().syntax_errors.append(msg)
                    print("A syntax error is found at index " + str(token_indexes[0]) + ", token " + symbol[
                        'token'] + ".")
                    print("Information: curr_state", stack[-1], "on input '", symbol['grammar_symbol'], "'")

                    # panic mode
                    panic_mode = True
                    while panic_mode:
                        top = stack[-2]
                        if len(top.children) == 0:
                            stack.pop()
                            stack.pop()
                            continue

                        found_end_of_line = False
                        for child in top.children:
                            if type(child.value) != dict:
                                continue
                            if child.value['token'] == '\n':    #TODO create a list of rhs of the grammar that are stops
                                panic_mode = False
                                found_end_of_line = True
                                break

                        if found_end_of_line is False:
                            stack.pop()
                            stack.pop()

                    while True:
                        token_indexes = lexical.next()
                        symbol = SymbolTable.getInstance().unknown_tokens[token_indexes[0]]
                        if symbol['token'] == '\n':
                            token_indexes = lexical.next()
                            break

                    symbol = SymbolTable.getInstance().unknown_tokens[token_indexes[0]]
                    grammar_symbol = symbol['token']

                    if symbol['grammar_symbol'] is not None:
                        grammar_symbol = symbol['grammar_symbol']
                    action = slr1[stack[-1]][grammar_symbol]

                if action.type is ActionType.SHIFT:
                    node = Tree()
                    node.value = symbol
                    stack.append(node)
                    stack.append(action.next_state)
                    token_indexes = lexical.next()
                elif action.type is ActionType.GOTO:
                    raise Exception("Unexpected action type: GOTO! GOTO should only be after reduce action!")
                elif action.type is ActionType.REDUCE:
                    parent = Tree()
                    reduce_rule = action.reduce_rule
                    parent.value = reduce_rule[0]
                    rhs_length = len(reduce_rule) - 2

                    for x in range(rhs_length):
                        stack.pop()
                        child = stack.pop()
                        parent.children.insert(0, child)

                    action = slr1[stack[-1]][reduce_rule[0]]
                    if action.type is not ActionType.GOTO:
                        raise Exception("Unexpected action type: " + action.type.name + "! Should be GOTO action!")

                    stack.append(parent)
                    stack.append(action.next_state)
                elif action.type is ActionType.ACCEPT:
                    parse_tree = stack[-1]
                    print("Syntax analysis is complete!")
                    return parse_tree
        except EOFError:
            print("Found the end of input!")
            grammar_symbol = "EoI"
            while True:
                action = slr1[stack[-1]][grammar_symbol]
                if action.type is ActionType.ACCEPT:
                    parse_tree = stack[-2]
                    print("Syntax analysis is complete!")
                    return parse_tree

                parent = Tree()
                reduce_rule = action.reduce_rule
                parent.value = reduce_rule[0]
                rhs_length = len(reduce_rule) - 2

                for x in range(rhs_length):
                    stack.pop()
                    child = stack.pop()
                    parent.children.insert(0, child)

                action = slr1[stack[-1]][reduce_rule[0]]

                if action.type is not ActionType.GOTO:
                    raise Exception("Unexpected action type: " + action.type.name + "! Should be GOTO action!")

                stack.append(parent)
                stack.append(action.next_state)
        except KeyError:
            print("Key is not found in the symbol table! ", lexical.lexemes[token_indexes[0]: token_indexes[1]])
