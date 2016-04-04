Simulations of Magnetohydrodynamic Waves Driven by Photospheric Motions
=======================================================================


Code: [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.48891.svg)](http://dx.doi.org/10.5281/zenodo.48891)
Thesis: [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.48888.svg)](http://dx.doi.org/10.5281/zenodo.48888)



This is the PhD Thesis of Stuart Mumford.

Quick Start
--------------

To build this thesis you should be able to run:

    git clone git@gitlab.com:Cadair/Thesis.git
    cd Thesis
    git annex get
    conda env create -f conda_requirements.yml
    source activate thesis
    python run.py thesis
    
This assumes a few things:

1. You have pythontex, pdfLaTeX and bibtex.
2. You have conda installed.
3. You have an ssh key configured for GitLab
4. You have git-annex installed.

If you need more information continue reading!

Information
-----------

This is based on the thesis template [here](https://github.com/kks32/phd-thesis-template).
To run this you need Python 2.7 with PythonTex, PDFLaTeX and BibTeX.
The Python dependencies needed are given in `conda_requirements.txt`.

### Using conda

You can build the thesis from inside a conda environment as long as you have 
TexLive and pythontex installed in your system path. You can create a conda 
environment with the following command:

`conda env create -f conda_requirements.yml`

activate the new environment with:

`source activate thesis`

### Obtaining the data

The data needed to run the Python code in this thesis is managed using [git-annex](https://git-annex.branchable.com/).
Firstly, therefore, you will need to [install git-annex](https://git-annex.branchable.com/install/).

Once you have installed git-annex you will need to have the
[GitLab Repository](https://gitlab.com/Cadair/Thesis) as a remote, as this hosts
the git-annex data. If you have already cloned from GitHub you will need to run:

    git remote add gitlab git@gitlab.com:Cadair/Thesis.git
    
**NOTE:** You must have an ssh key configured on GitLab for git-annex to work.
If you have cloned directly from the GitLab repository you can skip this step.

once you have this remote run:

    git fetch --all
    git annex get

to download the data.

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

The actual content of the document is made availble under the terms of the
CC-BY 4.0 license. The contents of Chapter 4 form part of [Mumford et. al
(2015)](http://dx.doi.org/10.1088/0004-637X/799/1/6) and is subject to the
license of that journal. Permission for the material to be included and
distributed as part of this thesis has been obtained, but derivative works are
a murky area.

