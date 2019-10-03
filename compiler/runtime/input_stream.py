from compiler.error_handler.error_handler import ErrorHandler
from compiler.lexical.valid_token_fsm import ValidTokenFSM


class InputStream:
    intput_stream = []

    @staticmethod
    def transform_to_token_and_store_to_input_stream(inputs):
        for input_token in inputs:
            converted_token = input_token
            if ValidTokenFSM.is_bool(input_token):
                input_type = 'BOOL'
                grammar_symbol = 'BLIT'
            elif ValidTokenFSM.is_int(input_token):
                input_type = 'INT'
                grammar_symbol = 'ILIT'
                converted_token = int(converted_token)
            elif ValidTokenFSM.is_float(input_token):
                input_type = 'FLOAT'
                grammar_symbol = 'FLIT'
                converted_token = float(converted_token)
            elif ValidTokenFSM.is_string(input_token):
                input_type = 'STRING'
                grammar_symbol = 'SLIT'
            elif ValidTokenFSM.is_char(input_token):
                input_type = 'CHAR'
                grammar_symbol = 'CLIT'
            else:
                input_type = 'ERROR'
                grammar_symbol = 'ERROR'
                ErrorHandler.getInstance().warnings.append('Warning: unable to identify the input as literal!')

            grammar_token = {
                "uid": None,
                "token": converted_token,
                "grammar_symbol": grammar_symbol,
                "type": input_type,
                "value": input_token
            }
            InputStream.intput_stream.append(grammar_token)
