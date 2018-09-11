#!/bin/bash

python setup.py sdist --formats=tar

python setup.py build_sphinx -b confluence -a