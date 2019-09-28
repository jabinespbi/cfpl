class AbstractSyntaxTree:
    """Creates ast from parse tree"""

    @staticmethod
    def create_ast(parse_tree):
        """Convert parse tree to abstract syntax tree using depth first, left to right traversal."""
        ast = parse_tree.copy()

        done = []
        stack = [parse_tree]
        ast_stack = [ast]
        while len(stack) is not 0:
            top = stack[-1]
            ast_top = ast_stack[-1]
            if len(top.children) > 0:
                if top not in done:
                    for x in range(len(top.children) - 1, -1, -1):
                        stack.append(top.children[x])
                        ast_stack.append(ast_top.children[x])
                        done.append(top)
                else:
                    AbstractSyntaxTree.reduce(stack.pop(), ast_stack.pop())
            else:
                stack.pop()
                ast_stack.pop()

        return ast

    @staticmethod
    def reduce(parse_tree, ast):
        """Note: this process will not mutate the parse_tree and the ast will not reference the
        contents of the parse_tree. the parse_tree is only included to know the rule to which it will reduce."""
        rule = [parse_tree.value, "->"]
        # if tree.value['grammar_symbol'] is not None:
        #     rule[0] = tree.value['grammar_symbol']

        for child in parse_tree.children:
            if type(child.value) is dict:
                if child.value['grammar_symbol'] is not None:
                    rule.append(child.value['grammar_symbol'])
                else:
                    rule.append(child.value['token'])
            else:
                rule.append(child.value)

        if rule == ["<cfpl>", "->", "<declaration-list>", "<main-block>"]:
            ast.value = "CFPL"
            children = ast.children[0].children
            children.extend(ast.children[1].children)
            ast.children = children
        elif rule == ["<cfpl>", "->", "<declaration-list>"]:
            ast.value = "CFPL"
            ast.children = ast.children[0].children
        elif rule == ["<cfpl>", "->", "<main-block>"]:
            ast.value = "CFPL"
            ast.children = ast.children[0].children
        elif rule == ["<declaration-list>", "->", "<declaration>"]:
            pass
        elif rule == ["<declaration-list>", "->", "<declaration>", "<declaration-list>"]:
            executable_statement_list = ast.children[1].children
            ast.children.pop(1)
            ast.children.extend(executable_statement_list)
        elif rule == ["<declaration>", "->", "VAR", "<declaration-block-list>", "AS", "<data-type>", "\n"]:
            ast.value = "DECLARE"
            children = ast.children[1].children
            children.append(ast.children[3])
            ast.children = children
        elif rule == ["<declaration-block-list>", "->", "<declaration-block>"]:
            pass
        elif rule == ["<declaration-block-list>", "->", "<declaration-block>", ",", "<declaration-block-list>"]:
            executable_statement_list = ast.children[2].children
            ast.children.pop(1)
            ast.children.pop(1)
            ast.children.extend(executable_statement_list)
        elif rule == ["<declaration-block>", "->", "ID", "=", "<assignment>"]:
            ast.value = "="
            ast.children.pop(1)
        elif rule == ["<declaration-block>", "->", "ID"]:
            ast.value = ast.children[0].value
            ast.children.clear()
        elif rule == ["<data-type>", "->", "INT"] or \
                rule == ["<data-type>", "->", "CHAR"] or \
                rule == ["<data-type>", "->", "BOOL"] or \
                rule == ["<data-type>", "->", "FLOAT"]:
            ast.value = ast.children[0].value['token']
            ast.children.clear()
        elif rule == ["<main-block>", "->", "START", "\n", "STOP"]:
            ast.children.clear()
        elif rule == ["<main-block>", "->", "START", "\n", "STOP", "\n"]:
            ast.children.clear()
        elif rule == ["<main-block>", "->", "START", "\n", "<executable-statement-list>", "STOP"]:
            ast.children = ast.children[2].children
        elif rule == ["<main-block>", "->", "START", "\n", "<executable-statement-list>", "STOP", "\n"]:
            ast.children = ast.children[2].children
        elif rule == ["<executable-statement-list>", "->", "<executable-statement>"]:
            pass
        elif rule == ["<executable-statement-list>", "->", "<executable-statement>", "<executable-statement-list>"]:
            executable_statement_list = ast.children[1].children
            ast.children.pop(1)
            ast.children.extend(executable_statement_list)
        elif rule == ["<executable-statement>", "->", "ID", "=", "<assignment>", "\n"]:
            ast.value = "="
            ast.children.pop(3)
            ast.children.pop(1)
        elif rule == ["<executable-statement>", "->", "<output>", "\n"]:
            ast.value = ast.children[0].value
            ast.children = ast.children[0].children
        elif rule == ["<executable-statement>", "->", "<input>", "\n"]:
            ast.value = ast.children[0].value
            ast.children = ast.children[0].children
        elif rule == ["<executable-statement>", "->", "<while>", "\n"]:
            ast.value = ast.children[0].value
            ast.children = ast.children[0].children
        elif rule == ["<executable-statement>", "->", "<if>"]:
            raise Exception("Not implemented")
        elif rule == ["<while>", "->", "WHILE", "(", "<or-expression>", ")", "\n", "START", "\n", "<executable-statement-list>", "STOP"]:
            child1 = ast.children[2]
            child2 = ast.children[7]
            ast.children = []
            ast.children.append(child1)
            ast.children.append(child2)
            ast.value = "WHILE"
        elif rule == ["<if>", "->", "IF", "(", "<or-expression>", ")", "\n", "START", "\n", "<executable-statement-list>", "STOP", "\n"]:
            child1 = ast.children[2]
            child2 = ast.children[7]
            ast.children = []
            ast.children.append(child1)
            ast.children.append(child2)
            ast.value = "IF"
        elif rule == ["<if>", "->", "IF", "(", "<or-expression>", ")", "\n", "START", "\n", "<executable-statement-list>", "STOP", "\n", "<else>"]:
            child1 = ast.children[2]
            child2 = ast.children[7]
            child3 = ast.children[10]
            ast.children = []
            ast.children.append(child1)
            ast.children.append(child2)
            ast.children.append(child3)
            ast.value = "IF-ELSE"
        elif rule == ["<else>", "->", "ELSE", "\n", "START", "\n", "<executable-statement-list>", "STOP"]:
            ast.value = "ELSE"
            ast.children = ast.children[4].children
        elif rule == ["<assignment>", "->", "ID", "=", "<assignment>"]:
            ast.value = "="
            ast.children.pop(1)
        elif rule == ["<assignment>", "->", "<or-expression>"]:
            ast.value = ast.children[0].value
            ast.children = ast.children[0].children
        elif rule == ["<or-expression>", "->", "<or-expression>", "OR", "<and-expression>"]:
            ast.value = "OR"
            ast.children.pop(1)
        elif rule == ["<or-expression>", "->", "<and-expression>"]:
            ast.value = ast.children[0].value
            ast.children = ast.children[0].children
        elif rule == ["<and-expression>", "->", "<and-expression>", "AND", "<equality-expression>"]:
            ast.value = "AND"
            ast.children.pop(1)
        elif rule == ["<and-expression>", "->", "<equality-expression>"]:
            ast.value = ast.children[0].value
            ast.children = ast.children[0].children
        elif rule == ["<equality-expression>", "->", "<equality-expression>", "<equality-operator>",
                      "<relational-expression>"]:
            ast.value = ast.children[1].value
            ast.children.pop(1)
        elif rule == ["<equality-expression>", "->", "<relational-expression>"]:
            ast.value = ast.children[0].value
            ast.children = ast.children[0].children
        elif rule == ["<equality-operator>", "->", "=="] or \
                rule == ["<equality-operator>", "->", "<>"]:
            ast.value = ast.children[0].value['token']
            ast.children.clear()
        elif rule == ["<relational-expression>", "->", "<relational-expression>", "<relational-operator>",
                      "<additive-expression>"]:
            ast.value = ast.children[1].value
            ast.children.pop(1)
        elif rule == ["<relational-expression>", "->", "<additive-expression>"]:
            ast.value = ast.children[0].value
            ast.children = ast.children[0].children
        elif rule == ["<relational-operator>", "->", ">"] or \
                rule == ["<relational-operator>", "->", "<"] or \
                rule == ["<relational-operator>", "->", ">="] or \
                rule == ["<relational-operator>", "->", "<="]:
            ast.value = ast.children[0].value['token']
            ast.children.clear()
        elif rule == ["<additive-expression>", "->", "<additive-expression>", "<additive-operator>",
                      "<multiplicative-expression>"]:
            ast.value = ast.children[1].value
            ast.children.pop(1)
        elif rule == ["<additive-expression>", "->", "<multiplicative-expression>"]:
            ast.value = ast.children[0].value
            ast.children = ast.children[0].children
        elif rule == ["<additive-operator>", "->", "+"] or \
                rule == ["<additive-operator>", "->", "-"] or \
                rule == ["<additive-operator>", "->", "&"]:
            ast.value = ast.children[0].value['token']
            ast.children.clear()
        elif rule == ["<multiplicative-expression>", "->", "<multiplicative-expression>", "<multiplicative-operator>",
                      "<unary-expression>"]:
            ast.value = ast.children[1].value
            ast.children.pop(1)
        elif rule == ["<multiplicative-expression>", "->", "<unary-expression>"]:
            ast.value = ast.children[0].value
            ast.children = ast.children[0].children
        elif rule == ["<multiplicative-operator>", "->", "*"] or \
                rule == ["<multiplicative-operator>", "->", "/"] or \
                rule == ["<multiplicative-operator>", "->", "%"]:
            ast.value = ast.children[0].value['token']
            ast.children.clear()
        elif rule == ["<unary-expression>", "->", "<unary-operator>", "<unary-expression>"]:
            ast.value = ast.children[0].value
            ast.children.pop(0)
        elif rule == ["<unary-expression>", "->", "<parenthesis-expression>"]:
            ast.value = ast.children[0].value
            ast.children = ast.children[0].children
        elif rule == ["<unary-operator>", "->", "+"]:
            ast.value = "UNARY-PLUS"
            ast.children.clear()
        elif rule == ["<unary-operator>", "->", "-"]:
            ast.value = "UNARY-MINUS"
            ast.children.clear()
        elif rule == ["<unary-operator>", "->", "NOT"]:
            ast.value = "NOT"
            ast.children.clear()
        elif rule == ["<parenthesis-expression>", "->", "(", "<or-expression>", ")"]:
            ast.value = ast.children[1].value
            ast.children = ast.children[1].children
        elif rule == ["<parenthesis-expression>", "->", "ID"] or \
                rule == ["<parenthesis-expression>", "->", "CLIT"] or \
                rule == ["<parenthesis-expression>", "->", "ILIT"] or \
                rule == ["<parenthesis-expression>", "->", "FLIT"] or \
                rule == ["<parenthesis-expression>", "->", "BLIT"] or \
                rule == ["<parenthesis-expression>", "->", "SLIT"]:
            ast.value = ast.children[0].value
            ast.children.clear()
        elif rule == ["<output>", "->", "OUTPUT:", "<or-expression>"]:
            ast.value = "OUTPUT"
            ast.children.pop(0)
        elif rule == ["<input>", "->", "INPUT:", "<id-list>"]:
            ast.value = "INPUT"
            ast.children.pop(0)
            ast.children = ast.children[0].children
        elif rule == ["<id-list>", "->", "ID"]:
            pass  # ignore
        elif rule == ["<id-list>", "->", "<id-list>", ",", "ID"]:
            id_list = ast.children[0].children
            id_list.append(ast.children[1])
            ast.children = [id_list]
        else:
            raise Exception("Something went wrong during converting to AST! Found an unexpected production rule.")
