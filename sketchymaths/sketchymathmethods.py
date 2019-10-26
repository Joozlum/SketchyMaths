import math

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
    How To Add Custom Methods:
    
Let's say you have some function that you want to use, or if you have a list of constants
that frequently come up in your math ramblings that you want to be able to quickly call to.
As long as you know a little bit of python code, you can quickly add any method to
SketchyMaths here.
Below is a very basic example.

Create a def for the calculation.  
In SketchyMaths a try function is used, so if your method
returns an error, it won't run and crash the program.  Infinite loops, however, will likely
work as expected, causing the program to hang indefinitely.  If your method requires a loop,
just ensure that it has a well defined exit parameter.
"""
def percent(value):
    """
    Take a percent value and return it in decimal form.
    :param value: int or float
    :return: float
    """
    return value / 100


"""
Now that we have a function, we add it to the sketchy_dict.  The sketchy_dict is just 
a dictionary of key pairs that tell the code what to call if certain text appears in the 
evaluate function. Whatever you set the key to is what you will have to type into the 
equation.
 """
sketchy_dict['percent'] = percent  # add function call without parenthesis for dictionary.

""" 
Final note:  If you use a name that already is in sketchy_dict below it will be replaced.
Also, this being python, if you want to import code (e.g. random), then you can do that,
but just remember the evaluate function is updated frequently, so if your code doesn't
always return the same result, even when the inputs remain unchanged, you might run into
some strange behavior.
If you do import code, just remember to add it to sketchy_dict here so it will be called.
"""


def logic(*args, **kwargs):  #  More complicated example of custom method.  Allows for adding logic gates.
    """
    Simple logic gate construct that can take any number of inputs
    :param args: first arg is name of gate, all following args are input values
    :param kwargs: true=true_condition(default=1) false=false_condition(default=0)
    :return: boolean
    """
    true = 1
    if 'true' in kwargs:
        true = kwargs['true']
    false = 0
    if 'false' in kwargs:
        false = kwargs['false']

    gate_types = ['AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR', 'XNOR']

    #  args[0] is evaluated to find the name of the gate
    gate_type = str(args[0])
    gate_type = gate_type.upper()

    if gate_type not in gate_types:
        return "gate not recognized"

    if gate_type == 'AND':
        for arg in args[1:]:  # tests all args excluding the first, as it is the gate name
            if arg != true:
                return False
        return True
    if gate_type == 'OR':
        for arg in args[1:]:
            if arg == true:
                return True
        return False
    if gate_type == 'NOT':  # since a NOT gate only takes one argument, any extra will be ignored
        for arg in args[1:]:
            if arg == true:
                return False
            else:
                return True
    if gate_type == 'NAND':
        for arg in args[1:]:
            if arg == false:
                return True
        return False
    if gate_type == 'NOR':
        for arg in args[1:]:
            if arg == true:
                return False
        return True
    if gate_type == 'XOR':
        x = None
        for arg in args[1:]:
            if x is None:
                if arg == true:
                    x = True
                if arg == false:
                    x = False
            if arg == true:
                if x is False:
                    return True
            if arg == false:
                if x is True:
                    return True
        return False

    if gate_type == 'XNOR':
        x = None
        for arg in args[1:]:
            if x is None:
                if arg == true:
                    x = True
                if arg == false:
                    x = False
            if arg == true:
                if x is False:
                    return False
            if arg == false:
                if x is True:
                    return False
        return True


sketchy_dict['logic'] = logic


def filter_logic(test, true_result, false_result):  #  Very basic function to compliment logic
    """
    Function to take in a bool and return a custom value for true or false
    :param test: bool
    :param true_result:
    :param false_result:
    :return:
    """
    if test:
        return true_result
    else:
        return false_result


sketchy_dict['filter_logic'] = filter_logic
