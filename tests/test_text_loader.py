import unittest
import os
from sketchymaths.internalsketch.text_loader import load_text

class LoadTextTestCase(unittest.TestCase):
    def setUp(self):
        path = os.getcwd().split('\\')
        if path[-1] == 'tests':
            del path[-1]
        path.append('sketchymaths')
        path.append('internalsketch')
        with open('\\'.join(path)+'\\Guide.txt') as guide_file:
            self.guide_text = guide_file.read()
        with open('\\'.join(path) + '\\Methods.txt') as methods_file:
            self.methods_text = methods_file.read()

    def test_loading_guide(self):
        result = load_text('guide')
        self.assertEqual(result, self.guide_text, 'Error loading Guide.txt!')

    def test_loading_methods(self):
        result = load_text('methods')
        self.assertEqual(result, self.methods_text, 'Error loading Methods.txt!')

    def test_loading_file_not_found(self):
        result = load_text('no_file')
        self.assertEqual(result, 'Text not found!', 'Error with text_loader!')