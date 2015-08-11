from setuptools import setup, find_packages

import roboticsrov

REQUIREMENTS = [
    'pyserial>=2.7',
    'roboticsnet'
]

DEPENDENCY_LINKS = [
    'git+https://github.com/space-concordia-robotics/robotics-networking/tarball/master#egg=roboticsnet-0.0.1'
]

setup(
    name='roboticsrov',
    version=roboticsrov.__version__,

    description='',
    long_description=open('README.rst').read(),
    url='http://www.github.com/space-concordia-robotics/robotics-rover',
    license='MIT',

    author='TBD',

    install_requires = REQUIREMENTS,
    dependency_links = DEPENDENCY_LINKS,

    packages=['roboticsrov'],
    zip_safe=False,
    scripts=['roboticsrov/bin/roboticsrov-test']
)

