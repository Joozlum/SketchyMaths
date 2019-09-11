"""
Custom code for debugging and logging information about how the program runs
"""
import time


# Code to clone SketchyBook into SketchyExamples
#   Decided to separated the books so that updating or pulling a branch down doesn't clear the user's book
# book = shelve.open('../data/SketchyBook')
# book_copy = shelve.open('../data/SketchyExamples')
# for key in book.keys():
#     book_copy[key] = book[key]
#
# book.close()
# book_copy.close()

#  decorator that works for (most) class functions to give log data on
#  these can be added by putting @SketchCollection('label') before a function
#  'label' can be any string, and is what the logger calls any information
#  collected from it.
#  Any method or class function that is used in binding calls throws an error.
class SketchCollection(object):
    def __init__(self, name=None, *args, **kwargs):
        self.func = name
        self.calls = 0
        self.total_time = 0

    @property
    def average_time(self):
        if self.calls > 0:
            return self.total_time/self.calls

    def __call__(self, f):

        @self.timer()
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapper

    def timer(self):

        def outer_wrap(f):

            def inner_wrap(*args, **kwargs):
                self.calls += 1
                start_time = time.perf_counter()
                call_type = f(*args, **kwargs)
                elapsed_time = time.perf_counter() - start_time
                self.total_time += elapsed_time
                print('{}\n{}, {}, {}'.format(self.func, self.calls, self.total_time, self.average_time))
                return call_type
            return inner_wrap
        return outer_wrap




