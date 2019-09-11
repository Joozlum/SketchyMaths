#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kivy
kivy.require('1.11.1')
from sketchymaths.sketchymathsapp import SketchyMathsApp

#  Disable multitouch
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')

if __name__ == "__main__":
    SketchyMathsApp().run()
