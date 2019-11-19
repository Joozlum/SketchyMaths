"""
SketchyTypes are modifiers for how to display outputs.

The clearest example is money.

If a '$' is found in an output, then round it to two decimal places,
but always display two decimal places, and add the $ sign before the
value.

"""

sketchy_types = []

entry = {
    'key': '$',  # key is what to look for in equation_text
    'remove_key': True,  # should the key be removed from evaluation?
    'position': 0,  # where to look, 0 beginning, -1 end, None is all
    'code': None,  #  code to run over number
    'type': [int, float],  #  what types it has to be
    'format': "{:,.2f}",  # formatting code to run number through
    'before': '$',  # string to place before number
    'after': ''  # string to place after number
}
sketchy_types.append(entry)

