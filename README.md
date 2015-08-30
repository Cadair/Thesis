Simulations of Magnetohydrodynamic Waves Driven by Photospheric Motions
=======================================================================

This is the PhD Thesis of Stuart Mumford.


Information
-----------

This is based on the thesis template [here](https://github.com/kks32/phd-thesis-template).
To run this you need Python 2.7 with PythonTex, PDFLaTeX and BibTeX.
The dependancies needed are given in `conda_requirements.txt`, the following
packages are specific or need specific versions:

* [matplotlib](http://matplotlib.org/) >= 1.5.dev
* [texfigure](https://github.com/Cadair/texfigure)
* [pysac](https://github.com/SWAT-Sheffield/pysac)

### Using conda

You can build the thesis from inside a conda environment as long as you have 
TexLive and pythontex installed in your system path. You can create a conda 
environment with the following command:

`conda create -n thesis --file conda_requirements.txt`

activate the new environment with:

`source activate thesis`

### Obtaining the data

Currently this is not accessible without my ssh key.


### Building the Thesis

Once the data has been obtained and the environment built, you can build the
pdf with the following command:

`python run.py thesis`

This will produce a file: `thesis/smumford_thesis.pdf`.


Copyright
---------

The LaTeX and Python source code in this repository are copyright Krishna Kumar or Stuart Mumford
and are released under the MIT licence. The content of the thesis is a much more copyright murky
area, with some of it having been published and therefore copyright the journal it was published in
etc. If you wish to reuse any figures or content from the thesis, the safest option is to contact
Stuart.

