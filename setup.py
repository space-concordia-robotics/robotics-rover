from setuptools import setup, find_packages

import roboticsrov

REQUIREMENTS = [
    'pyserial>=2.7',
]


setup(
    name='roboticsrov',
    version=roboticsrov.__version__,

    description='',
    long_description=open('README.rst').read(),
    # url='http://www.github.com/psyomn/pypsylbm',
    license='MIT',

    author='TBD',

    install_requires = REQUIREMENTS,

    packages=['roboticsrov'],
    zip_safe=False,
    scripts=['roboticsrov/bin/roboticsrov-test']
)

