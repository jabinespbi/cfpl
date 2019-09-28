from compiler.error_handler.error_handler import ErrorHandler
from compiler.semantics.action_type import ActionType
from compiler.symbols.symbol_table import SymbolTable
from compiler.tree import Tree
from compiler.utils import Utils


class ParseTree:
    """This is the syntax analysis part of the compiler.
    Creates the parse tree using the slr1 parsing table"""

    # list of rhs that stops the panic mode (e.g. rules with '\n')
    _panic_mode_rhs_list = [
        "<cfpl>",
        "<declaration-list>",
        "<declaration>",
        "<executable-statement-list>"
        "<executable-statement>"
    ]

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
                    msg = "A syntax error is found near \"" + Utils.near(lexical.lexemes, token_indexes[
                        0]) + "\" at line " + str(Utils.line_number(lexical.lexemes, token_indexes[0]))
                    ErrorHandler.getInstance().syntax_errors.append(msg)
                    print("A syntax error is found at index " + str(token_indexes[0]) + ", token " + symbol[
                        'token'] + ".")
                    print("Information: curr_state", stack[-1], "on input '", symbol['grammar_symbol'], "'")

                    ParseTree.panic_mode(lexical, stack, symbol['token'])
                    token_indexes = lexical.next()
                    continue

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
                if action is None:
                    msg = "A syntax error is found near \"" + Utils.near(lexical.lexemes, len(lexical.lexemes) - 1) + \
                          "\" at line " + str(Utils.line_number(lexical.lexemes, token_indexes[0]))
                    ErrorHandler.getInstance().syntax_errors.append(msg)
                    print("A syntax error is found at index EoI")
                    return None

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

    @staticmethod
    def panic_mode(lexical, stack, current_token):
        """current token is used if \n then, there is no need to sync the lexical"""
        # panic mode
        panic_mode = True
        while panic_mode:
            state0 = 0
            if stack[-1] == state0:
                break

            top = stack[-2]
            if type(top.value) is dict:
                if top.value['token'] == "\n":
                    break

            if top.value in ParseTree._panic_mode_rhs_list:
                break
            else:
                stack.pop()
                stack.pop()

        if current_token != '\n':
            while True:
                token_indexes = lexical.next()
                symbol = SymbolTable.getInstance().unknown_tokens[token_indexes[0]]
                if symbol['token'] == '\n':
                    break
