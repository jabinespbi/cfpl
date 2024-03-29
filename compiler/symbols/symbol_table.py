class SymbolTable:
    """"""
    __instance = None

    @staticmethod
    def getInstance():
        if SymbolTable.__instance is None:
            SymbolTable()
        return SymbolTable.__instance

    def __init__(self):
        if SymbolTable.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SymbolTable.__instance = self
            self.unknown_tokens = {}   # tokens such as variables, literals, etc. are not known to grammar
            self.symbol_table = {}  # list of declared variables
