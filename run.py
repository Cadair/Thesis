#!/usr/bin/env python2
"""
Run code, analyis or build documents related to this repository

Usage:
    run.py thesis [--rerun=RR] [--view] [--viewer=PDF]
    run.py download

Options:
    --view  Compile and then open pdf.
    --viewer=PDF  PDF Viewer. [default: evince]
    --rerun=RR PythonTeX rerun flag. [default: modified]

"""
from __future__ import print_function

import os
import sys
import bz2
import subprocess

try:
    import docopt
except ImportError:
    from scripts.extern import docopt

try:
    import progressbar
except ImportError:
    from scripts.extern import progressbar

try:
    import requests
except ImportError:
    from scripts.extern import requests

os.chdir(os.path.dirname(os.path.realpath(__file__)))

arguments = docopt.docopt(__doc__, version='1.0.0')

#Fix rerun bug
if arguments['--rerun'] is None:
    arguments['--rerun'] = 'modified'

file_prefix = 'smumford_thesis'
#Compile Paper
if arguments['thesis']:
    os.chdir('thesis')
    os.system('pdflatex -shell-escape -interaction=batchmode {}.tex'.format(file_prefix))
    os.system('pythontex.py --interpreter python:python2 {}.tex --rerun={}'.format(file_prefix, arguments['--rerun']))
    os.system('bibtex {}'.format(file_prefix))
    os.system('makeindex {}.aux'.format(file_prefix))
    os.system('makeindex {}.idx'.format(file_prefix))
    os.system('makeindex {0}.nlo -s nomencl.ist -o {0}.nls'.format(file_prefix))
    os.system('pdflatex --shell-escape -interaction=batchmode {}.tex'.format(file_prefix))
    os.system('makeindex {0}.nlo -s nomencl.ist -o {0}.nls'.format(file_prefix))
    os.system('pdflatex --shell-escape -interaction=batchmode {}.tex'.format(file_prefix))
    if arguments['--view']:
        os.system('{} {}.pdf'.format(arguments['--viewer'], file_prefix))
    os.chdir('../')

#Download data
if arguments['download']:
    print("Nothing to Download")
