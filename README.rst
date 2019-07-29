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

* TODO
    * Create settings window
    * Create method for customizing names of equation separate from id

Usage
-----

Launching the app
~~~~~~~~~~~~~~~~~

`Kivy` is compatible with Python 2 as well as Python 3::

    cd sketchymaths
    python main.py

Running the testsuite
~~~~~~~~~~~~~~~~~~~~~

Run its testsuite either with Python3::

    cd sketchymaths
    python -m unittest discover

Or with `nose`::

    cd sketchymaths
    nosetests

Or with `py.test`::

    cd sketchymaths
    py.test

Deploying to Android
~~~~~~~~~~~~~~~~~~~~

You can easily run the app on Android by using the `Kivy Launcher`.


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
