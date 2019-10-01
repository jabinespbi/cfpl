from compiler.error_handler.error_handler import ErrorHandler
from compiler.symbols.symbol_table import SymbolTable
from compiler.utils import Utils


class Semantics:
    """Checks type mismatch, undeclared variable, reserved identifier misuse, and multiple declaration of
        variable """

    @staticmethod
    def check(original_ast):
        SymbolTable.getInstance().symbol_table.clear()
        ast = original_ast.copy()

        done = []  # already push to stack
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
                        error_msg = "Incompatible types " + child.value['token'] + "!"
                        ErrorHandler.getInstance().semantics_errors.append(error_msg)

                if Utils.is_declared(child.value):
                    error_msg = "Variable " + child.value['token'] + " is already defined!"
                    ErrorHandler.getInstance().semantics_errors.append(error_msg)

                child.value['type'] = data_type
                SymbolTable.getInstance().symbol_table[child.value['token']] = child.value
        elif tree.value == "OUTPUT":
            child = tree.children[0]
            if Utils.is_id(child.value):
                if Utils.is_declared(child.value) is False:
                    error_msg = "Cannot resolve symbol " + child.value['token'] + "!"
                    ErrorHandler.getInstance().semantics_errors.append(error_msg)
        elif tree.value == "INPUT":
            for child in tree.children:
                if Utils.is_declared(child.value) is False:
                    error_msg = "Cannot resolve symbol " + child.value['token'] + "!"
                    ErrorHandler.getInstance().semantics_errors.append(error_msg)
        elif tree.value == "IF" or tree.value == "IF-ELSE" or tree.value == "WHILE":
            condition = tree.children[0]
            error_msgs = Semantics.check_type_operand(condition, "BOOL")
            if len(error_msgs) > 0:
                if Utils.is_id(condition.value):
                    if Utils.is_declared(condition.value):
                        ErrorHandler.getInstance().semantics_errors.append(error_msgs)
                    else:
                        error_msg = "Cannot resolve symbol " + condition.value['token'] + "!"
                        ErrorHandler.getInstance().semantics_errors.append(error_msg)
                else:
                    ErrorHandler.getInstance().semantics_errors.append(error_msgs)
        elif tree.value == "DO" or tree.value == "ELSE":
            pass
        elif tree.value == "ASSIGN":
            if Utils.is_id(tree.children[0].value):
                if Utils.is_declared(tree.children[0].value) is False:
                    error_msg = "Cannot resolve symbol " + tree.children[0].value['token'] + "!"
                    ErrorHandler.getInstance().semantics_errors.append(error_msg)
            else:
                raise Exception("Syntax analysis should have produce a syntax error to avoid this in semantics!")
        elif tree.value == "=":
            grammar_symbol = tree.children[1].value['grammar_symbol']
            if Utils.is_id(tree.children[1].value):
                if Utils.is_declared(tree.children[1].value) is False:
                    error_msg = "Cannot resolve symbol " + tree.children[1].value['token'] + "!"
                    ErrorHandler.getInstance().semantics_errors.append(error_msg)
                else:
                    symbol = SymbolTable.getInstance().symbol_table[tree.children[1].value['token']]
                    if symbol['type'] is None:
                        error_msg = "Unexpected no type for token " + tree.children[1].value['token'] + "!"
                        ErrorHandler.getInstance().semantics_errors.append(error_msg)
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
                error_msg = "Incompatible types " + tree.children[0].value['token'] + "!"
                ErrorHandler.getInstance().semantics_errors.append(error_msg)
            tree.value = tree.children[0].value
            tree.children.clear()
        elif tree.value == "OR" or \
                tree.value == "AND":
            Semantics.process_semantic_boolean_expression(tree)
        elif tree.value == "==" or \
                tree.value == "<>" or \
                tree.value == ">" or \
                tree.value == "<" or \
                tree.value == ">=" or \
                tree.value == "<=":
            Semantics.process_semantic_relational_expression(tree)
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
            operand1 = tree.children[0]
            error_msgs_int = Semantics.check_type_operand(operand1, "INT")
            error_msgs_float = Semantics.check_type_operand(operand1, "FLOAT")

            if len(error_msgs_int) > 0 and len(error_msgs_float) > 0:
                ErrorHandler.getInstance().semantics_errors.append(
                    "Expected INT or FLOAT type for" + operand1.value['token'] + "!")
                tree.value = {
                    "uid": None,
                    "token": None,
                    "grammar_symbol": "ERROR",
                    "type": None,
                    "value": None
                }
            elif len(error_msgs_int) == 0:
                tree.value = {
                    "uid": None,
                    "token": None,
                    "grammar_symbol": "ILIT",
                    "type": None,
                    "value": None
                }
            elif len(error_msgs_float) == 0:
                tree.value = {
                    "uid": None,
                    "token": None,
                    "grammar_symbol": "FLIT",
                    "type": None,
                    "value": None
                }
        elif tree.value == "NOT":
            operand1 = tree.children[0]
            error_msgs = Semantics.check_type_operand(operand1, "BOOL")

            if len(error_msgs) > 0:
                ErrorHandler.getInstance().semantics_errors.append(error_msgs)
                tree.value = {
                    "uid": None,
                    "token": None,
                    "grammar_symbol": "ERROR",
                    "type": None,
                    "value": None
                }
            else:
                tree.value = {
                    "uid": None,
                    "token": None,
                    "grammar_symbol": "BLIT",
                    "type": None,
                    "value": None
                }
        else:
            raise Exception("Couldn't find the semantic rules of the ast node value " + tree.value + "!" +
                            " Maybe it should be included or not?")

    @staticmethod
    def process_semantic_math_expression(tree):
        operand1 = tree.children[0]
        operand2 = tree.children[1]
        error_msgs_float1 = Semantics.check_type_operand(operand1, "FLOAT")
        error_msgs_float2 = Semantics.check_type_operand(operand2, "FLOAT")
        error_msgs1 = Semantics.check_type_operand(operand1, "INT")
        error_msgs1.extend(Semantics.check_type_operand(operand1, "FLOAT"))
        error_msgs2 = Semantics.check_type_operand(operand2, "INT")
        error_msgs2.extend(Semantics.check_type_operand(operand2, "FLOAT"))

        if len(error_msgs1) > 1 or len(error_msgs2) > 1:
            error_msg = "Operator " + tree.value + " can only be applied to int and float types! "
            ErrorHandler.getInstance().semantics_errors.append(error_msg)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": "ERROR",
                "type": None,
                "value": None
            }
        elif len(error_msgs_float1) == 0 or \
                len(error_msgs_float2) == 0:
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": "FLIT",
                "type": None,
                "value": None
            }
        else:
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": "ILIT",
                "type": None,
                "value": None
            }

    @staticmethod
    def process_semantic_boolean_expression(tree):
        operand1 = tree.children[0]
        operand2 = tree.children[1]
        error_msgs = Semantics.check_type_operand(operand1, "BOOL")
        error_msgs.extend(Semantics.check_type_operand(operand2, "BOOL"))

        if len(error_msgs) > 0:
            ErrorHandler.getInstance().semantics_errors.append(error_msgs)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": "ERROR",
                "type": None,
                "value": None
            }
        else:
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": "BLIT",
                "type": None,
                "value": None
            }

    @staticmethod
    def process_semantic_relational_expression(tree):
        operand1 = tree.children[0]
        operand2 = tree.children[1]
        error_msgs1 = Semantics.check_type_operand(operand1, "INT")
        error_msgs1.extend(Semantics.check_type_operand(operand1, "FLOAT"))
        error_msgs2 = Semantics.check_type_operand(operand2, "INT")
        error_msgs2.extend(Semantics.check_type_operand(operand2, "FLOAT"))

        if len(error_msgs1) > 1 or len(error_msgs2) > 1:
            error_msg = "Operator " + tree.value + " can only be applied to int and float types! "
            ErrorHandler.getInstance().semantics_errors.append(error_msg)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": "ERROR",
                "type": None,
                "value": None
            }
        else:
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": "BLIT",
                "type": None,
                "value": None
            }

    @staticmethod
    def process_semantic_string_expression(tree):
        """Allow all types for string expression"""
        tree.value = {
            "uid": None,
            "token": None,
            "grammar_symbol": "SLIT",
            "type": None,
            "value": None
        }

    @staticmethod
    def check_type_operand(operand, data_type):
        """ignores with grammar symbol of ERROR"""
        error_messages = []
        if Utils.is_id(operand.value):
            if Utils.is_declared(operand.value) is False:
                error_messages.append("Cannot resolve symbol " + str(operand.value['token']) + "!")
            elif Utils.is_id_of_type(operand.value, data_type) is False:
                error_messages.append("Expected " + data_type + " type for " + str(operand.value['token']) + "!")
        elif Utils.is_literal_of_type(operand.value, data_type) is False:
            error_messages.append("Expected " + data_type + " type for " + str(operand.value['token']) + "!")

        return error_messages
