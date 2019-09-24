from compiler.error_handler.error_handler import ErrorHandler
from compiler.symbols.symbol_table import SymbolTable


class Semantics:
    """Checks type mismatch, undeclared variable, reserved identifier misuse, and multiple declaration of
        variable """

    @staticmethod
    def check(original_ast):
        SymbolTable.getInstance().symbol_table.clear()
        ast = original_ast.copy()

        done = []
        stack = [ast]
        while len(stack) is not 0:
            top = stack[-1]
            if len(top.children) > 0:
                if top not in done:
                    for x in range(len(top.children) - 1, -1, -1):
                        stack.append(top.children[x])
                        done.append(top)
                else:
                    Semantics.check_by_semantic_rules(stack.pop())
            else:
                stack.pop()

        return ast

    @staticmethod
    def check_by_semantic_rules(tree):
        if tree.value == "CFPL":
            pass
        elif tree.value == "DECLARE":
            data_type = tree.children.pop().value
            for child in tree.children:
                if child.value['type'] is not None:
                    if child.value['type'] != data_type:
                        print("Incompatible types ", child.value['token'], "!")
                child.value['type'] = data_type
                SymbolTable.getInstance().symbol_table[child.value['token']] = child.value
        elif tree.value == "OUTPUT":
            pass
        elif tree.value == "INPUT":
            for child in tree.children:
                if child.value['token'] not in SymbolTable.getInstance().symbol_table:
                    ErrorHandler.getInstance().errors.append("Cannot resolve symbol ", child.value['token'], "!")
        elif tree.value == "=":
            grammar_symbol = tree.children[1].value['grammar_symbol']
            if grammar_symbol is "ID":
                if tree.children[1].value['token'] not in SymbolTable.getInstance().symbol_table:
                    print("Cannot resolve symbol ", tree.children[1].value['token'], "!")
                if tree.children[1].value['type'] is None:
                    print("Unexpected no type for token ", tree.children[1].value['token'], "!")
                tree.children[0].value['type'] = tree.children[1].value['type']
            elif grammar_symbol is "CLIT":
                tree.children[0].value['type'] = "CHAR"
            elif grammar_symbol is "ILIT":
                tree.children[0].value['type'] = "INT"
            elif grammar_symbol is "FLIT":
                tree.children[0].value['type'] = "FLOAT"
            elif grammar_symbol is "BLIT":
                tree.children[0].value['type'] = "BOOL"
            elif grammar_symbol is "SLIT":
                print("Incompatible types ", tree.children[0].value['token'], "!")
            tree.value = tree.children[0].value
            tree.children.clear()
        elif tree.value == "OR" or \
                tree.value == "AND" or \
                tree.value == "==" or \
                tree.value == "<>" or \
                tree.value == ">" or \
                tree.value == "<" or \
                tree.value == ">=" or \
                tree.value == "<=":
            Semantics.process_semantic_boolean_expression(tree)
        elif tree.value == "&":
            Semantics.process_semantic_string_expression(tree)
        elif tree.value == "+" or \
                tree.value == "-" or \
                tree.value == "*" or \
                tree.value == "/" or \
                tree.value == "%":
            Semantics.process_semantic_math_expression(tree)
        elif tree.value == "UNARY-MINUS" or \
                tree.value == "UNARY-PLUS":
            if tree.children[0].value['grammar_symbol'] == "ID":
                if tree.children[0].value['token'] in SymbolTable.getInstance().symbol_table:
                    if tree.children[0].value['type'] != "INT":
                        print("Operator ", tree.value, " cannot be applied to not ", tree.children[0].value['type'],
                              " type!")
                    else:
                        tree.value = {
                            "uid": None,
                            "token": None,
                            "grammar_symbol": "ILIT",
                            "type": None,
                            "value": None
                        }
                else:
                    print("Cannot resolve symbol ", tree.children[0].value['token'], "!")
            elif tree.children[0].value['grammar_symbol'] == "ILIT":
                tree.value = {
                    "uid": None,
                    "token": None,
                    "grammar_symbol": "ILIT",
                    "type": None,
                    "value": None
                }
            else:
                print("Operator ", tree.value, " cannot be applied to not INT type!")
        elif tree.value == "NOT":
            if tree.children[0].value['grammar_symbol'] == "ID":
                if tree.children[0].value['token'] in SymbolTable.getInstance().symbol_table:
                    if tree.children[0].value['type'] != "BOOL":
                        print("Operator ", tree.value, " cannot be applied to not ", tree.children[0].value['type'],
                              " type!")
                    else:
                        tree.value = {
                            "uid": None,
                            "token": None,
                            "grammar_symbol": "BLIT",
                            "type": None,
                            "value": None
                        }
                else:
                    print("Cannot resolve symbol ", tree.children[0].value['token'], "!")
            elif tree.children[0].value['grammar_symbol'] == "BLIT":
                tree.value = {
                    "uid": None,
                    "token": None,
                    "grammar_symbol": "BLIT",
                    "type": None,
                    "value": None
                }
            else:
                print("Operator ", tree.value, " cannot be applied to not BOOL type!")
        else:
            raise Exception("Couldn't find the semantic rules of the ast node value ", tree.value, "!",
                            " Maybe it should be included or not?")

    @staticmethod
    def process_semantic_math_expression(tree):
        operand1 = tree.children[0]
        operand2 = tree.children[1]
        if operand1.value['grammar_symbol'] == "ILIT" and \
                operand2.value['grammar_symbol'] == "ILIT":
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": "ILIT",
                "type": None,
                "value": None
            }
        elif operand1.value['grammar_symbol'] == "ID" and \
                operand2.value['grammar_symbol'] == "ID":
            if operand1.value['token'] not in SymbolTable.getInstance().symbol_table:
                print("Cannot resolve symbol ", operand1.value['token'], "!")

            if operand2.value['token'] not in SymbolTable.getInstance().symbol_table:
                print("Cannot resolve symbol ", operand2.value['token'], "!")

            if operand1.value['type'] != "INT" or \
                    operand2.value['type'] != "INT":
                print("Operator ", tree.value, " cannot be applied to not INT type!")
            else:
                tree.value = {
                    "uid": None,
                    "token": None,
                    "grammar_symbol": "ILIT",
                    "type": None,
                    "value": None
                }
        elif operand1.value['grammar_symbol'] == "ILIT" and \
                operand2.value['grammar_symbol'] == "ID":
            if operand2.value['token'] not in SymbolTable.getInstance().symbol_table:
                print("Cannot resolve symbol ", operand2.value['token'], "!")

            if operand2.value['type'] != "INT":
                print("Operator ", tree.value, " cannot be applied to not INT type!")
            else:
                tree.value = {
                    "uid": None,
                    "token": None,
                    "grammar_symbol": "ILIT",
                    "type": None,
                    "value": None
                }
        elif operand1.value['grammar_symbol'] == "ID" and \
                operand2.value['grammar_symbol'] == "ILIT":
            if operand1.value['token'] not in SymbolTable.getInstance().symbol_table:
                print("Cannot resolve symbol ", operand1.value['token'], "!")

            if operand1.value['type'] != "INT":
                print("Operator ", tree.value, " cannot be applied to not INT type!")
            else:
                tree.value = {
                    "uid": None,
                    "token": None,
                    "grammar_symbol": "ILIT",
                    "type": None,
                    "value": None
                }
        else:
            print("Operator ", tree.value, " cannot be applied to not INT type!")

    @staticmethod
    def process_semantic_boolean_expression(tree):
        operand1 = tree.children[0]
        operand2 = tree.children[1]
        if operand1.value['grammar_symbol'] == "BLIT" and \
                operand2.value['grammar_symbol'] == "BLIT":
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": "BLIT",
                "type": None,
                "value": None
            }
        elif operand1.value['grammar_symbol'] == "ID" and \
                operand2.value['grammar_symbol'] == "ID":
            if operand1.value['token'] not in SymbolTable.getInstance().symbol_table:
                print("Cannot resolve symbol ", operand1.value['token'], "!")

            if operand2.value['token'] not in SymbolTable.getInstance().symbol_table:
                print("Cannot resolve symbol ", operand2.value['token'], "!")

            if operand1.value['type'] != "BOOL" or \
                    operand2.value['type'] != "BOOL":
                print("Operator ", tree.value, " cannot be applied to not BOOL type!")
            else:
                tree.value = {
                    "uid": None,
                    "token": None,
                    "grammar_symbol": "BLIT",
                    "type": None,
                    "value": None
                }
        elif operand1.value['grammar_symbol'] == "BLIT" and \
                operand2.value['grammar_symbol'] == "ID":
            if operand2.value['token'] not in SymbolTable.getInstance().symbol_table:
                print("Cannot resolve symbol ", operand2.value['token'], "!")

            if operand2.value['type'] != "BOOL":
                print("Operator ", tree.value, " cannot be applied to not BOOL type!")
            else:
                tree.value = {
                    "uid": None,
                    "token": None,
                    "grammar_symbol": "BLIT",
                    "type": None,
                    "value": None
                }
        elif operand1.value['grammar_symbol'] == "ID" and \
                operand2.value['grammar_symbol'] == "BLIT":
            if operand1.value['token'] not in SymbolTable.getInstance().symbol_table:
                print("Cannot resolve symbol ", operand1.value['token'], "!")

            if operand1.value['type'] != "BOOL":
                print("Operator ", tree.value, " cannot be applied to not BOOL type!")
            else:
                tree.value = {
                    "uid": None,
                    "token": None,
                    "grammar_symbol": "BLIT",
                    "type": None,
                    "value": None
                }
        else:
            print("Operator ", tree.value, " cannot be applied to not BOOL type!")

    @staticmethod
    def process_semantic_string_expression(tree):
        operand1 = tree.children[0]
        operand2 = tree.children[1]

        error_msgs = []
        if operand1.value['grammar_symbol'] == "ID":
            if operand1.value['token'] not in SymbolTable.getInstance().symbol_table:
                error_msgs.append("Cannot resolve symbol ", operand1.value['token'], "!")

        if operand2.value['grammar_symbol'] == "ID":
            if operand2.value['token'] not in SymbolTable.getInstance().symbol_table:
                error_msgs += "Cannot resolve symbol ", operand2.value['token'], "!"

        if len(error_msgs) != 0:
            ErrorHandler.getInstance().errors.extend(error_msgs)
        else:
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": "SLIT",
                "type": None,
                "value": None
            }
