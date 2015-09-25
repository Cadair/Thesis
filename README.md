Simulations of Magnetohydrodynamic Waves Driven by Photospheric Motions
=======================================================================

This is the PhD Thesis of Stuart Mumford.


Information
-----------

This is based on the thesis template [here](https://github.com/kks32/phd-thesis-template).
To run this you need Python 2.7 with PythonTex, PDFLaTeX and BibTeX.
The dependancies needed are given in `conda_requirements.txt`, the following
packages need to be installed in addition to the ones given in the 
conda requirements folder:

* [matplotlib](http://matplotlib.org/) >= 1.5.dev
* [texfigure](https://github.com/Cadair/texfigure)
* [pysac](https://github.com/SWAT-Sheffield/pysac)
* [colormath](https://pypi.python.org/pypi/colormath/)

### Using conda

You can build the thesis from inside a conda environment as long as you have 
TexLive and pythontex installed in your system path. You can create a conda 
environment with the following command:

`conda create -n thesis --file conda_requirements.txt`

activate the new environment with:

`source activate thesis`

### Obtaining the data

Currently this is not accessible without my ssh key. This will be fixed as soon
as I can work out a techincal way of doing it, and I have had a break.


### Building the Thesis

Once the data has been obtained and the environment built, you can build the
pdf with the following command:

`python run.py thesis`

This will produce a file: `thesis/smumford_thesis.pdf`.


Copyright
---------

The LaTeX [here](https://github.com/kks32/phd-thesis-template) I used is 
copyright Krishna Kumar and licensed under the terms of the MIT licence. All
LaTeX code (not embedded Python) is licenced under the MIT license.
All Python code contained in this repository is copyright Stuart Mumford and 
is made availble under the MIT or 2-clause BSD license.

The actually content of the document is made availble under the terms of the
CC-BY 4.0 license. The contents of Chapter 4 form part of [Mumford et. al
(2015)](http://dx.doi.org/10.1088/0004-637X/799/1/6) and is subject to the
license of that journal. Permission for the material to be included and
distributed as part of this thesis has been obtained, but derivative works are
a murky area.

