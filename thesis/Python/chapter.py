# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 18:01:51 2014

@author: Stuart Mumford

A Class that holds Python information on a chapter level.
"""
import os
import sys
from collections import OrderedDict

import matplotlib.pyplot as plt

from plotting_helpers import fig_str, sub_fig_str, get_pgf_include

class Chapter(object):
    """
    A class holding information about different things in this chapter.
    """
    
    def __init__(self, pytex, number, chapter_path):
        self.pytex = pytex
        self._number = number
        self._chapter_path = chapter_path
        
        # Add this chapters Python dir to the sys path
        self.python_dir = os.path.join(self.chapter_path, 'Python')
        if not os.path.exists(self.python_dir):
            os.makedirs(self.python_dir)
        sys.path.append(self.python_dir)
        
        self.data_dir = os.path.join(self.chapter_path, 'Data')
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.fig_dir = os.path.join(self.chapter_path, 'Figs')
        if not os.path.exists(self.fig_dir):
            os.makedirs(self.fig_dir)
        
        self.fig_count = 1
        self._figure_registry = OrderedDict()
    
    @property
    def number(self):
        return self._number
    
    @property
    def chapter_path(self):
        return self._chapter_path
    
    def data_file(self, file_name):
        """
        Get the full path of a data file in this chapters data directory,
        add it to the pytex tracked files.
        
        Parameters
        ----------
        file_name : str
            The filename in the data directory
        """
        
        fname = os.path.join(self.data_dir, file_name)
        self.pytex.add_dependencies(fname)
        return fname
    
    def save_figure(self, ref, fig=None, fname=None):
        """
        Save a figure and track it in this chapter
        """
        
        if fig is None:
            fig = plt.gcf()
        
        if fname is None:
            fname = 'Chapter{}_Figure{}_{}'.format(self.number, self.fig_count,
                                                   ref)
    
        fname = os.path.join(self.fig_dir, fname)
        fig.savefig(fname)
        self.pytex.add_created(fname)
        
        self._figure_registry[ref] = {'number': self.fig_count, 'fname': fname}
        self.fig_count += 1
    
        return fname
    
    def get_figure(self, ref):
        """
        Get the filename of a figure that has already been saved
        
        Parameters
        ----------
        ref : str
            The Figure reference

        Returns
        -------
        fname : str
            The filename
        """

        return self._figure_registry[ref]['fname']
    
    def include_figure(self, ref, width=r"\columnwidth", **kwargs):
        """
        Print a whole figure environment
        """
        
        fname = self.get_figure(ref)
    
        default_kwargs = {'placement':'H', 'caption':'Figure {}'.format(ref),
                          'label':'fig:{}'.format(ref)}
        default_kwargs.update(kwargs)
        
        myfig = get_pgf_include(fname)

        return fig_str.format(myfig=myfig, **default_kwargs)