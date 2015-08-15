# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 14:47:19 2013

@author: Stuart Mumford

Plot THE graph.
"""

import os
import copy
import glob
import numpy as np
#import matplotlib_cust as mpc
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import OrderedDict


def get_combinations(tree_prefix):
    #==============================================================================
    # Define Search Parameters
    #==============================================================================
    driver = "*"
    post_amp = "A10"
    period = "p240"
    tube_s = "*"
    exp_fac = "*" # <-- To allow no exp_fac searches add _ to here
    data_dir = "%s/%s/%s_%s_%s%s/"%(tree_prefix,driver,period,post_amp,tube_s,exp_fac)

    #==============================================================================
    # Generate the combinations of parameters
    #==============================================================================
    dirs =  glob.glob(data_dir) #Find all the dirs in the tree matching the search.

    combinations = []
    for d in dirs:
        #Remove the prefix, remove leading and trailing slashes and then split on /
        s = d.partition(tree_prefix)[-1].strip('/').split('/')
        #The lowest dir will be in the p_A_r form, split them up.
        s2 = s[1].split('_')
        #Add all the parameters in one list to the combinations list
        combinations.append([s[0]] + s2)

        pars = combinations[-1]
        if pars[0] == 'Slog' and pars[4] != 'B005':
            combinations.pop(-1)
            continue
        if pars[3] == 'r45':
            combinations.pop(-1)
            continue

        if len(pars) < 5:
            pars += [None]

    return combinations


def load_files(tree_prefix, pars, wave_flux):

    if pars[4] is None:
        adir = "%s/%s/%s_%s_%s/"%(tree_prefix, pars[0], pars[1], pars[2], pars[3])
    else:
        adir = "%s/%s/%s_%s_%s_%s/"%(tree_prefix, pars[0], pars[1], pars[2], pars[3], pars[4])

#==============================================================================
# Wave FLux
#==============================================================================
    if wave_flux:
        if pars[4] is None:
            par = np.load(os.path.join(adir,"LineVar_%s_%s_%s_%s_Fwpar.npy"%(pars[0], pars[1], pars[2], pars[3])))
            perp = np.load(os.path.join(adir,"LineVar_%s_%s_%s_%s_Fwperp.npy"%(pars[0], pars[1], pars[2], pars[3])))
            phi = np.load(os.path.join(adir,"LineVar_%s_%s_%s_%s_Fwphi.npy"%(pars[0], pars[1], pars[2], pars[3])))
        else:
            par = np.load(os.path.join(adir,"LineVar_%s_%s_%s_%s_%s_Fwpar.npy"%(pars[0], pars[1], pars[2], pars[3], pars[4])))
            perp = np.load(os.path.join(adir,"LineVar_%s_%s_%s_%s_%s_Fwperp.npy"%(pars[0], pars[1], pars[2], pars[3], pars[4])))
            phi = np.load(os.path.join(adir,"LineVar_%s_%s_%s_%s_%s_Fwphi.npy"%(pars[0], pars[1], pars[2], pars[3], pars[4])))


        par = par **2
        perp = perp**2
        phi = phi**2

#==============================================================================
# Availible Flux
#==============================================================================
    else:
        par = np.load(os.path.join(adir,"LineFlux_%s_%s_%s_Fpar.npy"%(pars[0], pars[1], pars[2])))
        perp = np.load(os.path.join(adir,"LineFlux_%s_%s_%s_Fperp.npy"%(pars[0], pars[1], pars[2])))
        phi = np.load(os.path.join(adir,"LineFlux_%s_%s_%s_Fphi.npy"%(pars[0], pars[1], pars[2])))

    return par, perp, phi


def get_averages(tree_prefix, wave_flux=True):
    combinations = get_combinations(tree_prefix)

    drivers = {'Slog':[], 'Sarch':[], 'Suni':[], 'vert':[], 'horiz':[]}
    tube_rs = {'r10':copy.deepcopy(drivers), 'r30':copy.deepcopy(drivers), 'r60':copy.deepcopy(drivers)}

    for i, pars in enumerate(combinations):
        par, perp, phi = load_files(tree_prefix, pars, wave_flux)

        tot = par + perp + phi

        apar = (par / tot) * 100
        aperp = (perp / tot) * 100
        aphi = (phi / tot) * 100

        avgs = np.array([np.nanmean(apar), np.nanmean(aperp), np.nanmean(aphi)])
        avgs = np.round(avgs, decimals=1)

        tube_rs[pars[3]][pars[0]] = avgs

    return tube_rs


def make_flux_bar_chart(figsize, tree_prefix, wave_flux=True):

    combinations = get_combinations(tree_prefix)

    files = []
    for i,pars in enumerate(combinations):
    #    Flux_file = "Average_Fluxes_%s_%s_%s_%s.npy"%(pars[0], pars[1],
    #                                                  pars[2], pars[3])

        par, perp, phi = load_files(tree_prefix, pars, wave_flux)
    #==============================================================================
    # Other shit
    #==============================================================================

        tot = par + perp + phi

        apar = (par / tot) * 100
        aperp = (perp / tot) * 100
        aphi = (phi / tot) * 100

        avgs = [np.nanmean(apar), np.nanmean(aperp), np.nanmean(aphi)]
#        print pars[0], avgs, np.sum(avgs)

        if pars[4] is not None:
            pars[4] = '_'+pars[4]
        else:
            pars[4] = ''

        files.append(avgs)
    #    print pars
    #    files.append(os.path.join("%s/%s/%s_%s_%s%s/"%(tree_prefix,pars[0], pars[1],
    #                                                 pars[2], pars[3],pars[4]), Flux_file))


    #print len(files), len(combinations)


    combinations = np.array(combinations)
    drivers = np.array(list(set(combinations[:,0])))
    periods = np.array(list(set(combinations[:,1])))
    amplitudes = np.array(list(set(combinations[:,2])))
    radii = np.array(list(set(combinations[:,3])))
    radii = [radii[-1], radii[1], radii[0]]

    radii_labels = ["Tube Radius = %0.0f km"%(float(r.strip('r'))*15.6) for r in radii]

    fig, axes = plt.subplots(nrows=len(radii), ncols=1,sharex=True, figsize=figsize)
    plt.subplots_adjust(left=0.1,right=0.99,top=0.95,bottom=0.095)
    #fig.autofmt_xdate()
    for i, radius in enumerate(radii):
        index = (combinations[:,3]==radius).nonzero()[0]

        flux = OrderedDict()
        for k in index:
            flux.update({combinations[k,0]:files[k]})

#        for k,v in flux.items():
#            print k,v

    #    x = np.arange(0,len(flux.keys()))
        x = np.array([0,3,2,1,4])
    #    data = np.array(flux.values())
    #
    #    axes[i].bar(x, data[:,2],width=1,color='b',label=r"$F_\phi$")
    #    axes[i].bar(x, data[:,0],width=1,bottom=data[:,2],color='g',label=r"$F_\parallel$")
    #    axes[i].bar(x, data[:,1],width=1,bottom=data[:,0]+data[:,2],color='r',label=r"$F_\perp$")
    #    axes[i].bar(x, data[:,2],width=1,color='k',label=r"$F_\phi$", hatch='O',fill=False)
    #    axes[i].bar(x, data[:,0],width=1,bottom=data[:,2],color='k',label=r"$F_\parallel$", hatch='|',fill=False)
    #    axes[i].bar(x, data[:,1],width=1,bottom=data[:,0]+data[:,2],color='k',label=r"$F_\perp$", hatch='.',fill=False)


        for di, key in enumerate(['Slog', 'Sarch', 'Suni', 'horiz', 'vert']):
            b1 = axes[i].bar(di, flux[key][2],width=1,color='b')
            b2 = axes[i].bar(di, flux[key][0],width=1,bottom=flux[key][2],color='g')
            b3 = axes[i].bar(di, flux[key][1],width=1,bottom=flux[key][0]+flux[key][2],color='r')

    #        b1 = axes[i].bar(di, flux[key][2],width=1,color='k', hatch='O',fill=False)
    #        b2 = axes[i].bar(di, flux[key][0],width=1,bottom=flux[key][2],color='k', hatch='|',fill=False)
    #        b3 = axes[i].bar(di, flux[key][1],width=1,bottom=flux[key][0]+flux[key][2],color='k', hatch='.',fill=False)

        axes[i].xaxis.set_major_locator(mpl.ticker.FixedLocator(x+0.5))
        axes[i].xaxis.set_major_formatter(mpl.ticker.FixedFormatter( ['Logarithmic\nSpiral', 'Horizontal', 'Uniform\nSpiral', 'Archemedian\nSpiral', 'Vertical'] ))
        axes[i].set_ylim((0,100))
        axes[i].set_ylabel("Percentage Flux")
    #    axes[i].set_xlabel("Driver")
        axes[i].set_title(radii_labels[i])
#        mpc.thick_ticks(axes[i])

    #leg = axes[0].legend([b1, b2, b3][::-1], [r"$F_\phi$", r"$F_\parallel$", r"$F_\perp$"][::-1], fancybox=True)

    leg = axes[0].legend([b1, b2, b3][::-1], [r"$F_\phi^2$", r"$F_\parallel^2$", r"$F_\perp^2$"][::-1], fancybox=True)

    return fig

##plt.tight_layout()
#fig.savefig("%s_%s_Flux_comparision_BW.pdf"%(period,post_amp))
#plt.show()
