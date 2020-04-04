from sketchymaths.sketchymathmethods import sketchy_dict

def evaluate_equation_text(equation_text, internal=None):
    try:
        result = eval(equation_text, {'__builtins__': None}, sketchy_dict)
        error_message = ''
    except ArithmeticError as e:
        result = equation_text
        error_message = e
    except SyntaxError:
        result = equation_text
        error_message = None
    except EOFError as e:
        result = equation_text
        error_message = e
    except Exception as e:
        result = equation_text
        error_message = e
    return str(result), error_message
