# coding: utf-8
from __future__ import print_function

import os
import sys
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.image import NonUniformImage
from matplotlib import ticker

from scipy.interpolate import interp1d



def get_filepath(base_path, driver, period, post_amp, tube_r, exp_fac):
    if exp_fac is not None:
        data_dir = os.path.join(base_path, '%s/%s_%s_%s_%s/'%(driver, period, post_amp, tube_r, exp_fac))
    else:
        data_dir = os.path.join(base_path, '%s/%s_%s_%s/'%(driver, period, post_amp, tube_r))

    return data_dir


def get_data(base_path, driver, tube_r, exp_fac):

    post_amp = "A10"
    period = "p240"

    data_dir = get_filepath(base_path, driver, period, post_amp, tube_r, exp_fac)

    def path_join(filename):
        return os.path.join(data_dir, filename)

    all_svphi = np.load(path_join("LineVar_%s_%s_%s_vphi.npy"%(driver,period,post_amp))).T
    all_svperp = np.load(path_join("LineVar_%s_%s_%s_vperp.npy"%(driver,period,post_amp))).T
    all_svpar = np.load(path_join("LineVar_%s_%s_%s_vpar.npy"%(driver,period,post_amp))).T
    all_spoints = np.load(path_join("LineVar_%s_%s_%s_points.npy"%(driver,period,post_amp)))[:,::-1,:]
    all_times = np.load(path_join("LineVar_%s_%s_%s_times.npy"%(driver,period,post_amp)))[:,0]

    beta_line = np.load(path_join("LineFlux_%s_%s_%s_beta.npy"%(driver,period,post_amp))).T
    height_Mm = np.load(os.path.join(base_path, "heightMM.npy"))
    f = interp1d(np.linspace(0,128,128),height_Mm)
    y = f(all_spoints[0,:,2])

    if post_amp in ['A02k', 'A10']:
        data = [all_svpar * 1e3, all_svperp * 1e3, all_svphi * 1e3]
    else:
        data = [all_svpar, all_svperp, all_svphi]

    return y, data, beta_line, all_times, all_spoints


def get_speeds(base_path, driver, tube_r, exp_fac):

    post_amp = "A10"
    period = "p240"

    data_dir = get_filepath(base_path, driver, period, post_amp, tube_r, exp_fac)

    def path_join(filename):
        return os.path.join(data_dir, filename)

    cs_line = np.load(path_join("LineFlux_%s_%s_%s_cs.npy"%(driver,period,post_amp))).T
    va_line = np.load(path_join("LineFlux_%s_%s_%s_va.npy"%(driver,period,post_amp))).T

    return cs_line, va_line


def plot_paper1_td(data, all_times, y, beta_line, tube_r, fig_size=None):

    xxlim = -150
    x = all_times[:xxlim]
    lim = lambda vel: np.max([vel.max(),np.abs(vel.min())])
    def lim(vel):
        scope = np.median(vel) + 4 * np.std(np.array(vel))
        return scope
    def betaswap(b,pos):
        return "$%3.0f$"%(1./b)

    #cmap = 'gist_yarg'
    cmap = 'RdBu_r'

    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=fig_size)
    #plt.subplots_adjust(left=0.1,right=0.97,top=0.94,bottom=0.10)

    if tube_r == "r30":
        manual_locations = [(75, 1.4), (25, 1.0), (50, 0.2), (25, 0.01)]
    else:
        manual_locations = False


    colorbars = []
    for i in range(0,3):
        im = NonUniformImage(axes[i], interpolation='nearest', extent=[x.min(),x.max(),y.min(),y.max()], rasterized=True)
        im.set_cmap(cmap)
        im.set_clim(vmax=lim(data[i][:,:xxlim]),vmin=-lim(data[i][:,:xxlim]))
        im.set_data(x,y,np.array(data[i])[::-1,:xxlim])

        axes[i].images.append(im)
        axes[i].set_xlim(x.min(),x.max())
        axes[i].set_ylim(y.min(),y.max())
        colorbars.append(plt.colorbar(im,ax=axes[i],aspect=10))
        ct = axes[i].contour(x,y,beta_line[:,:xxlim],colors=['k'],levels=[1.,1/3.,1/5.,1/7.,1/10.,1/100.])
        plt.clabel(ct,fontsize=12,inline_spacing=1, manual=manual_locations,fmt=mpl.ticker.FuncFormatter(betaswap))

    colorbars[0].ax.set_ylabel(r"V$_\parallel$ [m/s]")
    colorbars[1].ax.set_ylabel(r"V$_\perp$ [m/s]")
    colorbars[2].ax.set_ylabel(r"V$_\phi$ [m/s]")

    #Labels
    axes[2].set_xlabel("Time [seconds]")
    #axes[0].set_ylabel("Height [Mm]")
    axes[1].set_ylabel("Height [Mm]")
    #axes[2].set_ylabel("Height [Mm]")

    yloc = ticker.MultipleLocator(base=0.4)
    [ax.yaxis.set_major_locator(yloc) for ax in axes]

    xloc = ticker.MultipleLocator(base=100)
    [ax.xaxis.set_major_locator(xloc) for ax in axes]

    for cbar in colorbars:
        cbar.locator = ticker.MaxNLocator(nbins=5)
        cbar.update_ticks()
        cbar.solids.set_edgecolor("face")
        #ax = cbar.ax.get_yaxis()
        #ax.set_major_locator(ticker.MaxNLocator(4, symmetric=True))

    return fig, axes


def overplot_speeds(axes, y, va_line, cs_line):
    delta_x = np.zeros(y.shape)
    delta_x[1:] = y[1:] - y[:-1]

    delta_t_va = delta_x*1e6 / va_line[:,0]
    delta_t_cs = delta_x*1e6 / cs_line[:,0]
    delta_t_vf = delta_x*1e6 / np.sqrt(cs_line[:,0]**2 + va_line[:,0]**2)
    delta_t_vs = delta_x*1e6 / np.sqrt(cs_line[:,0]**-2 + va_line[:,0]**-2)**-1

    ti = 60
    t_va = np.cumsum(delta_t_va) + ti
    t_cs = np.cumsum(delta_t_cs) + ti
    t_vf = np.cumsum(delta_t_vf) + ti
    t_vs = np.cumsum(delta_t_vs) + ti

    for i in range(0,3):
        axes[i].plot(t_va, y, label=r"$V_A$", linewidth=2, linestyle=':', color='k')#b
        axes[i].plot(t_cs, y, label=r"$C_s$", linewidth=2, linestyle='--', color='k')#g
        axes[i].plot(t_vf, y, label=r"$V_f$", linewidth=2, linestyle='-.', color='k')#r
        axes[i].plot(t_vs, y, label=r"$V_s$", linewidth=2, linestyle='-', color='k')#c


