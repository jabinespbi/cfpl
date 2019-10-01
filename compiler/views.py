import re

from django.shortcuts import render

from compiler.c_index_out_of_bounds_exception import CIndexOutOfBoundsException
from compiler.c_type_cast_exception import CTypeCastException
from compiler.error_handler.error_handler import ErrorHandler
from compiler.lexical.lexical import Lexical
from compiler.runtime.input_stream import InputStream
from compiler.runtime.output_stream import OutputStream
from compiler.runtime.runtime import Runtime
from compiler.semantics.grammar import Grammar
from compiler.semantics.yacc import Yacc


def index(request):

    tokens = None
    errors = []

    ErrorHandler.getInstance().clear_error_storage()
    OutputStream.output_stream = ""
    InputStream.intput_stream = []
    if request.POST and request.POST['source_code'] != '':
        inputs = request.POST['input'].split(',')
        InputStream.transform_to_token_and_store_to_input_stream(inputs)
        errors.extend(ErrorHandler.getInstance().warnings)
        source_code = request.POST['source_code']
        lexemes = source_code.replace("\r\n", "\n")
        lexical = Lexical(lexemes)
        tokens = lexical.get_all_tokens()
        errors.extend(ErrorHandler.getInstance().lex_errors)

        yacc = Yacc(Grammar.get_grammar(), lexemes)
        yacc.create_parser()
        yacc.create_parsing_table()
        yacc.create_parse_tree()
        errors.extend(ErrorHandler.getInstance().syntax_errors)

        if len(ErrorHandler.getInstance().syntax_errors) == 0:
            yacc.convert_parse_tree_to_abstract_syntax_tree()
            yacc.check_semantics()

            semantic_errors = ErrorHandler.getInstance().semantics_errors
            errors.extend(semantic_errors)
            if len(semantic_errors) == 0:
                runtime = Runtime()
                try:
                    runtime.run(yacc.ast)
                except CIndexOutOfBoundsException:
                    pass
                except CTypeCastException:
                    pass

                exceptions = ErrorHandler.getInstance().runtime_exceptions
                errors.extend(exceptions)

    context = {
        'tokens': tokens,
        'errors': errors,
        'output': OutputStream.output_stream
    }
    return render(request, 'compiler/index.html', context)
