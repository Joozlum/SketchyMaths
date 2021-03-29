from .evaluateequation import evaluate_equation_text

class EquationDict(dict):
    def uid_generator(self):
        """
        Generates a unique idea for equation_id
        :return:
            String in the format of a equation_id
        """
        i = 0
        while 'x' + str(i) in self.keys():
            i += 1
        return 'x' + str(i)


equation_dict = EquationDict()


class Equation:
    def __init__(self,
                 output_function=print,
                 equation_id=None,
                 delimiter=':'):

        # equations to update after this one
        self.links = set()

        # text to hold the equation formula
        self.equation_text = ''

        # value of equation after evaluation
        self.output = ''

        # function to call when outputting value
        self.output_function = output_function

        # character to surround references in equation_text
        self.delimiter = delimiter

        # holds whatever error messages evaluate_equation_text might return
        self.error_message = ''

        # used to prevent infinite looping during updates
        self.status = False

        # set name, if None generate new name
        if equation_id is None:
            self.equation_id = equation_dict.uid_generator()
        else:
            self.equation_id = equation_id

        # value to prevent loops.
        self.active = False

    def update_equation_dict(self):
        """
        Adds self to equation_dict using equation_id
        """
        equation_dict[self.equation_id] = self

    def update_equation_id(self, new_id):
        """
        Used for when equation_id changes
        """

        # Makes sure new_id is not blank and new_id is not already in equation_dict
        if not new_id or new_id in equation_dict.keys():
            return

        # can't have delimiter in equation_id in equation_id
        new_id = new_id.replace(self.delimiter, ';')

        # save old_id
        old_id = self.equation_id

        # delete old reference
        if old_id in equation_dict.keys():
            del equation_dict[old_id]

        # update instance equation_id property
        self.equation_id = new_id

        # add instance reference to equation_dict with new_id
        self.update_equation_dict()

        # replace old_id with new_id in any equations that link to this one
        for equation in self.links:
            self.get_equation(equation)._replace_updated_equation_ids(old_id, new_id)
        for equation in equation_dict.values():
            if old_id in equation.links:
                equation.links -= {old_id}
                equation.links |= {new_id}

    def _replace_updated_equation_ids(self, old_id, new_id):
        """"
        Replaces any old_id references with new_id references
        """
        self.equation_text = self.equation_text.replace(
            self.delimiter + old_id + self.delimiter,
            self.delimiter + new_id + self.delimiter
        )

    def update_text(self, new_text):
        """
        Called when changing equation_text
        """

        self.equation_text = new_text
        text_to_evaluate, references_to_update = self._prepare_equation()
        self._update_links(references_to_update)
        self.output, self.error_message = evaluate_equation_text(text_to_evaluate)
        if self.error_message:
            self.status = False
        else:
            self.status = True
        self.output_function()
        self.active = True  # prevents infinite loop if another equation tries to refresh this one during loop
        for equation in self.links:
            self.get_equation(equation).refresh()
        self.active = False

    def refresh(self):
        """
        Re-evaluates equation, used for updating equations when the referenced
        equations change.
        :return: None
        """
        if self.active:  # prevents from infinite loop
            return
        text_to_evaluate, references_to_update = self._prepare_equation()
        self.output, self.error_message = evaluate_equation_text(text_to_evaluate)
        self._update_links(references_to_update)
        if self.error_message:
            self.status = False
        else:
            self.status = True
        self.output_function()
        self.active = True
        for equation in self.links:
            self.get_equation(equation).refresh()
        self.active = False

    def _prepare_equation(self):
        """
        Prepares equation_text for running through evaluate_equation
        """
        text_to_evaluate = self.equation_text
        references = set()
        for equation_id in equation_dict.keys():
            if self.delimiter + equation_id + self.delimiter in text_to_evaluate:
                references |= {equation_id}
                text_to_evaluate = text_to_evaluate.replace(
                    self.delimiter + equation_id + self.delimiter,
                    str(equation_dict[equation_id].output)
                )
        return text_to_evaluate, references

    def _update_links(self, references):
        for equation in equation_dict.values():
            if equation.equation_id in references:
                equation.links |= {self.equation_id}
            else:
                equation.links -= {self.equation_id}

    @classmethod
    def get_equation(cls, equation_id):
        """
        Takes in equation_id string and returns Equation instance with that id
        :rtype: Equation
        """
        return equation_dict[equation_id]

    @classmethod
    def delete_equation(cls, equation_id):
        if equation_id in equation_dict.keys():
            del equation_dict[equation_id]



