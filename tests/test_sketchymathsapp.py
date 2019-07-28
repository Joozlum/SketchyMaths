#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from sketchymaths.sketchymathsapp import SketchyMathsApp


class TestSketchymathsApp(unittest.TestCase):
    """TestCase for SketchymathsApp.
    """
    def setUp(self):
        self.app = SketchyMathsApp()

    def test_name(self):
        self.assertEqual(self.app.name, 'sketchymaths')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
