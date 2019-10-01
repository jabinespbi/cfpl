class ErrorHandler:
    """"""
    __instance = None

    @staticmethod
    def getInstance():
        if ErrorHandler.__instance is None:
            ErrorHandler()
        return ErrorHandler.__instance

    def __init__(self):
        if ErrorHandler.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ErrorHandler.__instance = self
            self.warnings = []
            self.lex_errors = []
            self.syntax_errors = []
            self.semantics_errors = []
            self.runtime_exceptions = []

    def clear_error_storage(self):
        self.warnings = []
        self.lex_errors = []
        self.syntax_errors = []
        self.semantics_errors = []
        self.runtime_exceptions = []
