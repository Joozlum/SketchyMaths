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