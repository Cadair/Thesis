# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt

__all__ = ['fig_str', 'sub_fig_str', 'get_pgf_include']#, 'get_pgf_include', 'get_fig_env', 'get_subfig_env',
#           'make_fig_env', 'make_sub_figs']
#==============================================================================
# Latex helpers
#==============================================================================
# Some LaTeX code snippiets
fig_str = r"""
\begin{{figure*}}
    \centering
    {myfig}
    \caption{{{caption}}}
    \label{{{label}}}
\end{{figure*}}
"""

sub_fig_str = r"""\begin{{subfigure}}[{placement}]{{{width}}}
    {myfig}
    \caption{{{caption}}}
    \label{{{label}}}
\end{{subfigure}}"""

def get_pgf_include(fname, width=r"\columnwidth"):
    return r"\pgfimage[width={1}]{{{0}}}".format(fname, width)

def get_fig_env(figure_str, **kwargs):
    """
    Print a whole figure environment
    """
    global fig_count, fig_str

    default_kwargs = {'placement':'H', 'caption':'caption',
                      'label':'fig_{}'.format(fig_count)}

    default_kwargs.update(kwargs)

    return fig_str.format(myfig=figure_str, **default_kwargs)

def get_subfig_env(subfig_str, caption, label, subplacement='b',
                   subwidth=r'\textwidth'):

    return sub_fig.format(placement=subplacement, width=subwidth,
                          caption=caption, label=label, myfig=subfig_str)

def make_fig_env(cfg, **kwargs):
    fname = kwargs.pop('fname', None)
    fig = kwargs.pop('fig', None)
    width = kwargs.pop('width', r"\columnwidth")

    fname = save_fig(cfg, fig=fig, fname=fname)
    fig_str = get_pgf_include(fname, width=width)

    print(get_fig_env(fig_str, **kwargs))

    return fname

def make_sub_figs(cfg, figs, captions, labels=None, subplacement='b', subwidth=r'\textwidth',
                  subbefore='\n', subafter='\n', **kwargs):
    global fig_count

    if len(figs) != len(captions) != len(labels):
        raise ValueError("Please specify the same number of labels as figures")

    sub_figs_str = r""
    fnames = []

    if labels is None:
        labels = ['fig_{fig_count}']*len(figs)

    for fig, caption, label in itertools.izip(figs, captions, labels):
        fname = save_fig(cfg, fig=fig)
        fnames.append(fname)
        pgf = get_pgf_include(fname, width=subwidth)
        label = label.format(fig_count=fig_count)
        sub_figs_str += subbefore + get_subfig_env(pgf, caption, label,
                                                   subplacement=subplacement,
                                                  subwidth=subwidth) + subafter

    print(get_fig_env(sub_figs_str, **kwargs))
    return fnames
