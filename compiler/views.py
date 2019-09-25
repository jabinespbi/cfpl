from django.shortcuts import render

from compiler.error_handler.error_handler import ErrorHandler
from compiler.lexical.lexical import Lexical


def index(request):
    tokens = None
    errors = []

    errors = ErrorHandler.getInstance().lex_errors = []
    if request.POST:
        source_code = request.POST['source_code']
        lexemes = "\n".join(source_code.splitlines())
        lexical = Lexical(lexemes)
        tokens = lexical.get_all_tokens()
        errors = ErrorHandler.getInstance().lex_errors

    context = {
        'tokens': tokens,
        'errors': errors
    }
    return render(request, 'compiler/index.html', context)
