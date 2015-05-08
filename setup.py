from setuptools import setup, find_packages

import roboticsrov

setup(
    name='roboticsrov',
    version=roboticsrov.__version__,

    description='',
    long_description=open('README.rst').read(),
    # url='http://www.github.com/psyomn/pypsylbm',
    license='MIT',

    author='TBD',

    packages=['roboticsrov'],
    zip_safe=False,
    scripts=['roboticsrov/bin/roboticsrov-test']
)
