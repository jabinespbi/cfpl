class RuntimeList:
    """CFPL does not need a runtime stack because there is no functions, therefore no functions to be called
    and no functions to be pushed to the stack. Hence, this is just a list that keeps variables"""

    def __init__(self):
        self.variables = {}
        self.undeclared_variables = {}
