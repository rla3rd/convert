from setuptools import setup
from convert import __version__

setup( name='convert',
    description='automatic string conversion library',
    author='Rick Albright',
    version=__version__,
    py_modules=['convert', 'dateAdapter', 'pandas'],
    license='MIT License' )
