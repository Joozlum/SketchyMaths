=============================
SketchyMaths
=============================

MindMapping for Maths.  Allows for a blackboard style approach to
math, letting you have multiple math problems on the screen, while
also evaluating each in real time.  It also allows for taking the
result of one problem and using it in another, and if you change
any dependencies all of the problems that use them will update
with the changing results.


Features
--------
* Evaluates most mathematical equations
* Allows for multiple equations to be evaluated separately
* The result of one equation can be used in another equation.
* If one equation is changed any other equations dependant on it are also updated.


** TODO
    * Create settings window
    * Clean up code
    * Make arrows fancier and avoid crossing other equations

Usage
-----

Launching the app
~~~~~~~~~~~~~~~~~
Check requirements.txt to see if dependencies are installed.

`Kivy` is compatible with Python 2 as well as Python 3::

    cd sketchymaths
    python main.py

License
-------

Distributed under the terms of the `MIT license`, sketchymaths free and open source software


Issues
------

Report bugs at https://github.com/Joozlum/sketchymaths/issues.


.. _`Kivy Launcher`: http://kivy.org/docs/guide/packaging-android.html#packaging-your-application-for-the-kivy-launcher
.. _`Kivy`: https://github.com/kivy/kivy
.. _`MIT License`: http://opensource.org/licenses/MIT
.. _`nose`: https://github.com/nose-devs/nose/
.. _`py.test`: http://pytest.org/latest/
