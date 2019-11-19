import sketchymathmethods

"""
Equation class holds an equation, evaluates it and holds that evaluation
in the output.  The class also holds a dictionary containing references
to other equations.

Expected Behavior:

::Instance methods
    Store equation_text
        Public method for setting text

    Store equation_id
        Public method for setting id
            Would use private method for validating new name is unique
            Would also use a private class method to update any existing references


    Find links in equation_text and store them in list
        Private methods to do this internally
        This can be a staticmethod

    Replace links in equation_text with referenced output before evaluation
        Private methods
        Could possibly reuse method that finds links, or they could be combined
            (though i'm trying to keep everything simple)

    Evaluate and store output of equation
        Public method for retrieving output
        Private method for evaluating equation_text and getting output

    Method for retrieving output
        Public facing

::Class methods
    Store dictionary of {equation_id: reference}
        This could be controlled in private methods
        Private method for setting/changing equation_id
            Should prevent duplicate names
            Should update all references in other equation_text to reflect name

I think the issue i'm mulling over is more hung up on which functions go where.
Rather than thinking in public and private, my thoughts are more internal and
external.

The only methods that need external interaction would be:
    equation_text setter
        This would call all of the needed internal methods, but none of that needs
        to be accessed outside of the class.
    equation_id setter
        Same as equation_text, with the added need to ensure the name is unique,
        but that can be handled internally.
    update
        Call to update the output.
        If i handle controlling updates outside of class i'll need this.

    get_output
        Not sure this needs a method, since the output would never be changed
        externally, so it could just be called directly.
    get_links
        The function for drawing
    delete
        There would need to be a public facing method for deleting an equation,
        as the references inside of the class would also need to be cleared
"""

class Equation:
    equation_text = 'Enter some maths!'
    equation_id = ''
    output_text = 'Enter some maths!'
    delimiter = ':'
    links = []

    status = False

    _equations = {}

    #  list of equations that reference it so they update
    _references = set()

    def __init__(self, name=None, **kwargs):
        if not name:
            new_equation_id = self.uid_generator()
        else:
            new_equation_id = name
        self.equation_id = new_equation_id
        self.add_new_to_equations(new_equation_id, self)
        self.equation_text = "Enter some maths!"
        self.delimiter = ':'
        self.links = []
        self.status = False
        self._references = set()
        self.error = None
        self.type = None

    #  Public facing instance methods
    def set_text(self, text=None, starting_equation=None):
        if text:
            self.equation_text = text
            self._update_links()
        self.output_text = self.evaluate()
        if not starting_equation:
            starting_equation = self
        self.update_reference_outputs(starting_equation)
        # self.update_linked_outputs(self.equation_id)
        # self.print_all_references()

    def update_reference_outputs(self, starting_equation=None):
        for equation_id in self._references:
            equation = self.get_equation(equation_id)
            if equation == starting_equation:
                print('loop')
                return
            equation.set_text(text=None, starting_equation=starting_equation)

    def update_equation_id(self, new_id):
        old_id = self.equation_id
        if new_id == '':  #  Can't set name to None
            return

        if self.delimiter in new_id:
            new_id = new_id.replace(self.delimiter, ';')  # Can't have delimiter in id

        if self.test_link(new_id):  #  Return if name already exists
            return

        #  delete old entry from equations dictionary
        self.remove_equations_entry(old_id)

        #  add new id to _equations dictionary
        self.add_new_to_equations(new_id, self)

        self._update_all_equation_ids(old_id, new_id)

        #  update actual value
        self.equation_id = new_id

    def add_reference(self, equation_id):
        if equation_id in self.links:
            return
        self._references.update([equation_id])

    @classmethod
    def update_references(cls, equation_id, old_links, new_links):
        old = set(old_links)
        new = set(new_links)
        to_update = old.symmetric_difference(new)
        for new_reference in to_update.intersection(new):
            if cls.test_link(new_reference):
                cls.get_equation(new_reference).add_reference(equation_id)

        for old_reference in to_update.symmetric_difference(new):
            if cls.test_link(old_reference):
                cls.get_equation(old_reference).remove_reference(equation_id)

    def remove_reference(self, equation_id):
        self._references.difference_update([equation_id])

    @classmethod
    def remove_all_references(cls, equation_id):
        for equation in cls._equations.values():
            equation.remove_reference(equation_id)

    def get_references(self):
        references = []
        for equation_id in self._references:
            references.append(equation_id)
        return references

    @classmethod
    def print_all_references(cls):
        for equation in cls._equations.values():
            print(equation.equation_id, ':', equation.get_references(), 'links:', equation.links)

    @classmethod
    def get_linked_equations(cls, equation_id):
        """

        :param equation_id:
            String equation_id to search for links
        :return:
            list of equation instances with equation_id in links
        """
        linked_equations = []
        for inst in cls._equations.values():
            if equation_id in inst.links:
                linked_equations.append(inst)
        return linked_equations

    @classmethod
    def _update_all_equation_ids(cls, old_id, new_id):
        linked_equations = cls.get_linked_equations(old_id)
        for equation in linked_equations:
            new_equation_text = equation.equation_text.replace(
                cls.delimiter + old_id + cls.delimiter,
                cls.delimiter + new_id + cls.delimiter
            )
            #  This will run evaluation again
            #  Calling this will also update the links
            equation.set_text(new_equation_text)

    def _update_links(self):
        new_links = text_extract(self.equation_text)
        links = []
        for link in new_links:
            if self.test_link(link):
                links.append(link)
        self.update_references(self.equation_id, self.links, links)
        self.links = links
        return links

    # todo
    #   work out this function
    #   make sure it doesn't loop
    #   make sure all links have their output updated in correct order

    @classmethod
    def update_linked_outputs(cls, update_eid, internal=False, updated=None):
        if not updated:
            updated = [update_eid]
        if internal:
            updated.append(update_eid)
        for equation in cls._equations.values():
            if update_eid in equation.links:
                cls.update_linked_outputs(equation, internal=True, updated=updated)
                equation.output_text = equation.evaluate()

    def evaluate(self, internal=None):
        if '#' in self.equation_text:
            self.type = 'comment'
            return self.equation_text

        text_to_evaluate = self.replace_links_with_output()
        success = False
        try:
            result = eval(text_to_evaluate, {'__builtins__': None}, sketchymathmethods.sketchy_dict)
            self.type = type(result)
            success = True
            self.error = None
        except ArithmeticError as e:
            result = text_to_evaluate
            self.error = e
            self.type = None
        except SyntaxError:
            result = text_to_evaluate
            self.error = None
            self.type = None
        except EOFError as e:
            result = text_to_evaluate
            self.error = e
            self.type = None
        except Exception as e:
            result = text_to_evaluate
            self.error = e
            self.type = None

        self.status = success
        return str(result)

    def replace_links_with_output(self):
        output = self.equation_text
        for link in self.links:
            if self.test_link(link):
                output = output.replace(self.delimiter + link + self.delimiter,
                                        self.get_equation(link).output_text)
        return output


    @classmethod
    def add_new_to_equations(cls, equation_id, inst):
        cls._equations[equation_id] = inst

    @classmethod
    def test_link(cls, link):
        if link in cls._equations.keys():
            return True
        else:
            return False

    @classmethod
    def get_equation(cls, e_id):
        return cls._equations[e_id]

    @classmethod
    def remove_equations_entry(cls, equation_id):
        if cls.test_link(equation_id):
            del cls._equations[equation_id]

    @classmethod
    def uid_generator(cls):
        """
        Generates a unique idea for equation_id
        :return:
            String in the format of a equation_id
        """
        i = 0
        while 'x' + str(i) in cls._equations.keys():
            i += 1
        return 'x' + str(i)

    @classmethod
    def delete_equation(cls, equation_id):
        cls.remove_equations_entry(equation_id)
        for equation in cls._equations.values():
            equation.remove_reference(equation_id)

def text_extract(text, delimiter=':'):
    marks = []
    for char, x in zip(text, range(len(text))):
        if char == delimiter:
            marks.append(x)
    result = []
    while len(marks) > 1:
        result.append(text[marks.pop(0)+1:marks.pop(0)])

    return result

def chain_builder(starting_equation, loop=False, path=None):
    if loop:
        return ['loop']
    if path:
        if starting_equation.equation_id in path:
            loop = True
    if not path:
        path = [starting_equation.equation_id]
    else:
        path.append(starting_equation.equation_id)
    links = []
    for link in starting_equation.get_references():
        links.append(link)
        if link.references:
            links.extend(chain_builder(link.equation_id, loop=loop, path=path))
    return links
