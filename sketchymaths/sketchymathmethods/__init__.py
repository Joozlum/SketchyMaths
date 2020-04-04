import math
from .custom_method_tutorial import percent
from .factor import factor
from .base_n import base_n
from .logic import logic, filter_logic
sketchy_dict = {'acos': math.acos, 'asin': math.asin,
                'atan': math.atan, 'atan2': math.atan2, 'ceil': math.ceil,
                'cos': math.cos, 'cosh': math.cosh, 'degrees': math.degrees,
                'e': math.e, 'exp': math.exp, 'fabs': math.fabs, 'floor': math.floor,
                'fmod': math.fmod, 'frexp': math.frexp, 'hypot': math.hypot,
                'ldexp': math.ldexp, 'log': math.log, 'log10': math.log10,
                'modf': math.modf, 'pi': math.pi, 'pow': math.pow, 'radians': math.radians,
                'sin': math.sin, 'sinh': math.sinh, 'sqrt': math.sqrt, 'tan': math.tan, 'tanh': math.tanh,
                'bin': bin, 'sum': sum, 'zip': zip, 'range': range}

"""
To add a custom method, create a new python file in this folder, create the method, then import it and add it to the
sketchy_dict here.  Whatever name you give it will be what is used to call it within the program scope.
"""

sketchy_dict['percent'] = percent
sketchy_dict['factor'] = factor
sketchy_dict['base_n'] = base_n
sketchy_dict['logic'] = logic
sketchy_dict['filter_logic'] = filter_logic