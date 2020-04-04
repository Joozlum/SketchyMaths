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
Now that we have a function, we add it to the sketchy_dict.  To do this create a tuple or list with the
name as the first element and the custom method as the second.  Then go to the __init__.py file, import this
method, and then add it to the sketchy_dict
 """
custom_method = ('Percent', percent)  # add function call without parenthesis for dictionary.