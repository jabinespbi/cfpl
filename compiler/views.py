from django.shortcuts import render

from compiler.error_handler.error_handler import ErrorHandler
from compiler.lexical.lexical import Lexical
from compiler.semantics.grammar import Grammar
from compiler.semantics.yacc import Yacc


def index(request):
    tokens = None
    errors = []

    ErrorHandler.getInstance().lex_errors = []
    ErrorHandler.getInstance().syntax_errors = []
    if request.POST:
        source_code = request.POST['source_code']
        lexemes = "\n".join(source_code.splitlines())
        lexical = Lexical(lexemes)
        tokens = lexical.get_all_tokens()
        errors = ErrorHandler.getInstance().lex_errors

        yacc = Yacc(Grammar.get_grammar(), lexemes)
        yacc.create_parser()
        yacc.create_parsing_table()
        yacc.create_parse_tree()
        errors.extend(ErrorHandler.getInstance().syntax_errors)

        if len(ErrorHandler.getInstance().syntax_errors) == 0:
            yacc.convert_parse_tree_to_abstract_syntax_tree()

    context = {
        'tokens': tokens,
        'errors': errors
    }
    return render(request, 'compiler/index.html', context)
