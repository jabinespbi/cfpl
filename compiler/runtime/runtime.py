from compiler.c_index_out_of_bounds_exception import CIndexOutOfBoundsException
from compiler.c_type_cast_exception import CTypeCastException
from compiler.error_handler.error_handler import ErrorHandler
from compiler.runtime.input_stream import InputStream
from compiler.runtime.output_stream import OutputStream
from compiler.runtime.runtime_list import RuntimeList
from compiler.symbols.symbol_table import SymbolTable
from compiler.utils import Utils


class Runtime:

    def __init__(self):
        self.runtime_list = RuntimeList()

    def run(self, original_ast):
        rules_for_suspension = ['IF', 'IF-ELSE', 'WHILE']
        # if, if-else, and while nodes evaluation is suspended, and let the rules decide which nodes to visit
        ast = original_ast.copy()

        done = []  # already push to stack
        stack = [ast]
        while len(stack) is not 0:
            top = stack[-1]

            if len(top.children) > 0:
                if top.value in rules_for_suspension:
                    self.execute(stack.pop())
                elif top not in done:
                    for x in range(len(top.children) - 1, -1, -1):
                        stack.append(top.children[x])
                        done.append(top)
                else:
                    self.execute(stack.pop())
            else:
                stack.pop()

        return ast

    def run_with_side_effects(self, ast):
        rules_for_suspension = ['IF', 'IF-ELSE', 'WHILE']
        # if, if-else, and while nodes evaluation is suspended, and let the rules decide which nodes to visit

        done = []  # already push to stack
        stack = [ast]
        while len(stack) is not 0:
            top = stack[-1]

            if len(top.children) > 0:
                if top.value in rules_for_suspension:
                    self.execute(stack.pop())
                elif top not in done:
                    for x in range(len(top.children) - 1, -1, -1):
                        stack.append(top.children[x])
                        done.append(top)
                else:
                    self.execute(stack.pop())
            else:
                stack.pop()

        return ast

    def execute(self, tree):
        if tree.value == "CFPL":
            pass
        elif tree.value == "DECLARE":
            data_type = tree.children.pop().value
            for child in tree.children:
                if child.value['value'] is None:
                    child.value['type'] = data_type
                    if data_type == "INT":
                        child.value['value'] = 0
                    elif data_type == "CHAR":
                        child.value['value'] = ""
                    elif data_type == "BOOL":
                        child.value['value'] = "FALSE"
                    elif data_type == "FLOAT":
                        child.value['value'] = 0

                    self.runtime_list.variables[child.value['token']] = child.value
        elif tree.value == "OUTPUT":
            OutputStream.output_stream += self.get_python_string_value(tree.children[0].value)
        elif tree.value == "INPUT":
            for x in range(len(tree.children)):
                child = tree.children[x]
                if x >= len(InputStream.intput_stream):
                    exception = 'CIndexOutOfBoundsException: Index out of bounds is found at input! ' + str(x)
                    ErrorHandler.getInstance().runtime_exceptions.append(exception)
                    raise CIndexOutOfBoundsException('Index out of bounds is found at input! ' + str(x))

                input_token = InputStream.intput_stream[x]
                if Utils.is_id_of_type(child.value, input_token['type']) is False:
                    exception = 'CTypeCastException: Incompatible types between ' + child.value[
                        'token'] + ' and input # ' + str(x)
                    ErrorHandler.getInstance().runtime_exceptions.append(exception)
                    raise CTypeCastException(
                        'Incompatible types between ' + child.value['token'] + ' and input # ' + str(x))

                SymbolTable.getInstance().symbol_table['a']['value'] = input_token['token']
            # TODO: int and float mathematical operation with its storage capacity
        elif tree.value == "IF":
            condition = tree.children[0]
            self.run_with_side_effects(condition)
            value = self.get_python_value(condition.value)
            if value == True:
                self.run(tree.children[1])
            elif value == False:
                pass
            else:
                raise Exception("Expected to be a boolean value " + value + " !")
        elif tree.value == "IF-ELSE":
            condition = tree.children[0]
            self.run_with_side_effects(condition)
            value = self.get_python_value(condition.value)
            if value == True:
                self.run(tree.children[1])
            elif value == False:
                self.run(tree.children[2])
            else:
                raise Exception("Expected to be a boolean value " + value + " !")
        elif tree.value == "WHILE":
            condition = tree.children[0]
            while True:
                condition_copy = condition.copy()
                self.run_with_side_effects(condition_copy)
                value = self.get_python_value(condition_copy.value)
                if value == True:
                    self.run(tree.children[1])
                elif value == False:
                    break
                else:
                    raise Exception("Expected to be a boolean value " + value + " !")
        elif tree.value == "ASSIGN":
            pass
        elif tree.value == "DO" or tree.value == "ELSE":
            pass
        elif tree.value == "=":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value2 = self.get_python_value(operand2)
            if operand1['token'] in self.runtime_list.variables:
                variable = self.runtime_list.variables[operand1['token']]
                variable['value'] = value2
                tree.value = variable
                tree.children.clear()
            elif operand1['token'] in self.runtime_list.undeclared_variables:
                variable = self.runtime_list.undeclared_variables[operand1['token']]
                variable['value'] = value2
                tree.value = variable
                tree.children.clear()
            else:
                operand1['value'] = value2
                self.runtime_list.undeclared_variables[operand1['token']] = operand1
                tree.value = operand1
                tree.children.clear()
        elif tree.value == "OR":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_value(operand1)
            value2 = self.get_python_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "BOOL",
                "value": value1 or value2
            }
            tree.children.clear()
        elif tree.value == "AND":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_value(operand1)
            value2 = self.get_python_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "BOOL",
                "value": value1 and value2
            }
            tree.children.clear()
        elif tree.value == "==":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_value(operand1)
            value2 = self.get_python_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "BOOL",
                "value": value1 == value2
            }
            tree.children.clear()
        elif tree.value == "<>":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_value(operand1)
            value2 = self.get_python_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "BOOL",
                "value": value1 != value2
            }
            tree.children.clear()
        elif tree.value == ">":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_value(operand1)
            value2 = self.get_python_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "BOOL",
                "value": value1 > value2
            }
            tree.children.clear()
        elif tree.value == "<":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_value(operand1)
            value2 = self.get_python_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "BOOL",
                "value": value1 < value2
            }
            tree.children.clear()
        elif tree.value == ">=":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_value(operand1)
            value2 = self.get_python_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "BOOL",
                "value": value1 >= value2
            }
            tree.children.clear()
        elif tree.value == "<=":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_value(operand1)
            value2 = self.get_python_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "BOOL",
                "value": value1 <= value2
            }
            tree.children.clear()
        elif tree.value == "&":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_string_value(operand1)
            value2 = self.get_python_string_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "STRING",
                "value": value1 + value2  # value only used for ids
            }
            tree.children.clear()
        elif tree.value == "+":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_value(operand1)
            value2 = self.get_python_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "INT",
                "value": value1 + value2
            }
            tree.children.clear()
        elif tree.value == "-":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_value(operand1)
            value2 = self.get_python_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "INT",
                "value": value1 - value2
            }
            tree.children.clear()
        elif tree.value == "*":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_value(operand1)
            value2 = self.get_python_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "INT",
                "value": value1 * value2
            }
            tree.children.clear()
        elif tree.value == "/":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_value(operand1)
            value2 = self.get_python_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "INT",
                "value": value1 / value2  # TODO: throw exception if infinity
            }
            tree.children.clear()
        elif tree.value == "%":
            operand1 = tree.children[0].value
            operand2 = tree.children[1].value
            value1 = self.get_python_value(operand1)
            value2 = self.get_python_value(operand2)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "INT",
                "value": value1 % value2
            }
            tree.children.clear()
        elif tree.value == "UNARY-MINUS":
            operand1 = tree.children[0].value
            value1 = self.get_python_value(operand1)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "INT",
                "value": -value1
            }
            tree.children.clear()
        elif tree.value == "UNARY-PLUS":
            # TODO: unary minus and plus can be applied to float and int, change semantic analysis
            operand1 = tree.children[0].value
            value1 = self.get_python_value(operand1)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "INT",
                "value": +value1
            }
            tree.children.clear()
        elif tree.value == "NOT":
            operand1 = tree.children[0].value
            value1 = self.get_python_value(operand1)
            tree.value = {
                "uid": None,
                "token": None,
                "grammar_symbol": None,
                "type": "BOOL",
                "value": not value1
            }
            tree.children.clear()
        else:
            raise Exception("Couldn't find the runtime rules of the ast node value " + tree.value + "!" +
                            " Maybe it should be included or not?")

    def get_python_value(self, operand):
        if Utils.is_id(operand):
            return self.get_value_of_the_declared_or_undeclared_variable(operand)
        elif Utils.is_literal(operand):
            if operand['grammar_symbol'] == "CLIT":
                return operand['token']
            elif operand['grammar_symbol'] == "ILIT":
                return int(operand['token'])
            elif operand['grammar_symbol'] == "FLIT":
                return int(operand['token'])
            elif operand['grammar_symbol'] == "BLIT":
                if operand['token'] == '"FALSE"':
                    return False
                elif operand['token'] == '"TRUE"':
                    return True
                else:
                    raise Exception("Unexpected value for bool type! " + operand['token'])
            elif operand['grammar_symbol'] == "SLIT":
                return operand['token']
            else:
                raise Exception("Unexpected literal with grammar symbol " + operand['grammar_symbol'] + "!")
        elif operand['value'] is not None:
            return operand['value']

    def get_value_of_the_declared_or_undeclared_variable(self, variable):
        """variable should be a dictionary"""
        if type(variable) is not dict:
            raise Exception("Argument should be a dictionary!")

        if variable['token'] in self.runtime_list.variables:
            return self.runtime_list.variables[variable['token']]['value']
        elif variable['token'] in self.runtime_list.undeclared_variables:
            return self.runtime_list.undeclared_variables[variable['token']]['value']
        else:
            raise Exception("Couldn't find variable in undeclared and declared list")

    def get_python_string_value(self, operand):
        value = self.get_python_value(operand)
        if type(value) is bool:
            value = 'FALSE' if value is False else 'TRUE'
        elif type(value) is not str:
            value = str(value)
        else:
            value = value.replace('"', "")
            value = value.replace('\'', "")

        return value
