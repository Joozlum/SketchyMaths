import math

sketchy_dict = {'int': int, 'acos': math.acos, 'asin': math.asin,
             'atan': math.atan, 'atan2': math.atan2, 'ceil': math.ceil,
             'cos': math.cos, 'cosh': math.cosh, 'degrees': math.degrees,
             'e': math.e, 'exp': math.exp, 'fabs': math.fabs, 'floor': math.floor,
             'fmod': math.fmod, 'frexp': math.frexp, 'hypot': math.hypot,
             'ldexp': math.ldexp, 'log': math.log, 'log10': math.log10,
             'modf': math.modf, 'pi': math.pi, 'pow': math.pow, 'radians': math.radians,
             'sin': math.sin, 'sinh': math.sinh, 'sqrt': math.sqrt, 'tan': math.tan, 'tanh': math.tanh,
             'bin': bin}

#   Adding custom methods to equation evaluation.
#   Let's say you have some function that you want to use, or if you have a list of constants
#   that frequently come up in your math ramblings that you want to be able to quickly call to.
#   As long as you know a little bit of python code, you can quickly add any method to
#   MathJunk here.
#   Below is a very basic example.

#  Create a def for the calculation.  In MathJunk a try function is used, so if your method
#  returns an error, it won't run and crash the program.  Infinite loops, however, will likely
#  work as expected, causing the program to hang indefinitely.  If your method requires a loop,
#  just ensure that it has a well defined exit parameter.


def percent(value):  #  Our example here is simply returning a decimal for a percent.
    '''
    Returns a percent as decimal
    :param value:
    :return:
    '''
    return value/100

#  Now that we have a function, we add it to the junk_dict.  The junk_dict is just a dictionary
#  of key pairs that tell the code what to call if certain text appears in the evaluate function.
#  Whatever you set the key to is what you will have to type into the equation.

sketchy_dict['percent'] = percent  #  add function call without parenthesis for dictionary.

#  Final note:  If you use a name that already is in junk_dict below it will be replaced.
#   Also, this being python, if you want to import code (e.g. random), then you can do that,
#   but just remember the evaluate function is updated frequently, so if your code doesn't
#   always return the same result, even when the inputs remain unchanged, you might run into
#   some strange behavior.
#   If you do import code, just remember to add it to junk_dict here so it will be called.

