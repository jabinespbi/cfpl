from django.shortcuts import render

from compiler.lexical.lexical import Lexical


def index(request):
    tokens = None
    if request.POST:
        source_code = request.POST['source_code']
        lexemes = "\n".join(source_code.splitlines())
        lexical = Lexical(lexemes)
        tokens = lexical.get_all_tokens()

    context = {
        'tokens': tokens
    }
    return render(request, 'compiler/index.html', context)
