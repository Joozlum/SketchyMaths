import setuptools
from setuptools import setup

setup(
    name='SketchyMaths',
    version='0.9.0',
    packages=setuptools.find_packages(),
    package_data={'SketchyExamples': ['data/SketchyExamples.bak', 'data/SketchyExamples.dat', 'SketchyExamples.dir']},
    entry_point={'console_scripts': ['SketchyMaths:main']},
    url='https://github.com/Joozlum/SketchyMaths',
    license='',
    author='Joozlum',
    author_email='Ouzelum@gmail.com',
    description='Mind-Mapping for Maths'
)
