#!/opt/miniconda/envs/thesis/bin/python
#!/usr/bin/env python2
"""
Run code, analyis or build documents related to this repository

Usage:
    run.py paper [--rerun=RR] [--view] [--viewer=PDF]
    run.py thesis [--rerun=RR] [--view] [--viewer=PDF]
    run.py notebook [--port=P]

Options:
    --view  Compile and then open pdf.
    --viewer=PDF  PDF Viewer. [default: evince]
    --rerun=RR PythonTeX rerun flag. [default: errors]
    --port=P Port for IPython Notebook [default: 8898]

"""
from __future__ import print_function

import os
import sys
import bz2
import subprocess

import docopt

os.chdir(os.path.dirname(os.path.realpath(__file__)))

arguments = docopt.docopt(__doc__, version='1.0.0')

#Fix rerun bug
if arguments['--rerun'] is None:
    arguments['--rerun'] = 'errors'

file_prefix = 'smumford_thesis'
#Compile Paper
if arguments['paper'] or arguments['thesis']:
    os.chdir('thesis')
    os.system('pdflatex -shell-escape -interaction=batchmode {}.tex'.format(file_prefix))
    os.system('pythontex --interpreter python:{} {}.tex --rerun={}'.format(sys.executable, file_prefix, arguments['--rerun']))
    os.system('bibtex {}'.format(file_prefix))
    os.system('makeindex {}.aux'.format(file_prefix))
    os.system('makeindex {}.idx'.format(file_prefix))
    os.system('makeindex {0}.nlo -s nomencl.ist -o {0}.nls'.format(file_prefix))
    os.system('pdflatex --shell-escape -interaction=batchmode {}.tex'.format(file_prefix))
    os.system('makeindex {0}.nlo -s nomencl.ist -o {0}.nls'.format(file_prefix))
    os.system('pdflatex -synctex=1 --shell-escape -interaction=batchmode {}.tex'.format(file_prefix))
    if arguments['--view']:
        os.system('{} {}.pdf'.format(arguments['--viewer'], file_prefix))
    os.chdir('../')

if arguments['notebook']:
    if arguments['--port'] is None:
        arguments['--port'] = 8899
    import IPython
    IPython.start_ipython(['notebook', '--notebook-dir=notebooks',
    '--port={}'.format(arguments['--port'])])
