from setuptools import setup
from convert import __version__
 
setup( name='convert',
    description='automatic string conversion library',
    author='Richard Albright',
    version=__version__,
    py_modules=['convert', 'dateAdapter', 'xml2dict'],
    license='MIT License' )
