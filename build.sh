#!/bin/bash
cd $HOME/Dropbox/projects/convert
$PYTHON setup.py build
$PYTHON setup.py sdist
$PYTHON setup.py install
