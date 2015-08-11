# coding: utf-8
from __future__ import print_function

import os
from functools import partial
import numpy as np

from scipy.interpolate import interp1d


def get_filepath(base_path, driver, period, post_amp, tube_r, exp_fac):
    if exp_fac is not None:
        data_dir = os.path.join(base_path, '%s/%s_%s_%s_%s/'%(driver, period, post_amp, tube_r, exp_fac))
    else:
        data_dir = os.path.join(base_path, '%s/%s_%s_%s/'%(driver, period, post_amp, tube_r))

    return data_dir


def get_xy(base_path, driver, period, post_amp, tube_r, exp_fac):

    data_dir = get_filepath(base_path, driver, period, post_amp, tube_r, exp_fac)

    height_Mm = np.load(os.path.join(base_path, "heightMM.npy"))
    all_times = np.load(os.path.join(data_dir, ("LineVar_%s_%s_%s_times.npy"%(driver, period, post_amp))))[:,0]
    all_spoints = np.load(os.path.join(data_dir, "LineVar_%s_%s_%s_points.npy"%(driver,period,post_amp)))[:,::-1,:]

    f = interp1d(np.linspace(0,128,128), height_Mm)
    y = f(all_spoints[0,:,2])

    return all_times, y, all_spoints


def get_data(base_path, driver, period, post_amp, tube_r, exp_fac):

    data_dir = get_filepath(base_path, driver, period, post_amp, tube_r, exp_fac)

    path_join = partial(os.path.join, data_dir)

    all_svphi = np.load(path_join("LineVar_%s_%s_%s_vphi.npy"%(driver,period,post_amp))).T
    all_svperp = np.load(path_join("LineVar_%s_%s_%s_vperp.npy"%(driver,period,post_amp))).T
    all_svpar = np.load(path_join("LineVar_%s_%s_%s_vpar.npy"%(driver,period,post_amp))).T

    beta_line = np.load(path_join("LineFlux_%s_%s_%s_beta.npy"%(driver,period,post_amp))).T

    if post_amp in ['A02k', 'A10']:
        data = [all_svpar*1e3, all_svperp*1e3, all_svphi*1e3]
    else:
        data = [all_svpar, all_svperp, all_svphi]

    return data, beta_line


def get_speeds(base_path, driver, period, post_amp, tube_r, exp_fac):

    data_dir = get_filepath(base_path, driver, period, post_amp, tube_r, exp_fac)

    path_join = partial(os.path.join, data_dir)

    cs_line = np.load(path_join("LineFlux_%s_%s_%s_cs.npy"%(driver,period,post_amp))).T
    va_line = np.load(path_join("LineFlux_%s_%s_%s_va.npy"%(driver,period,post_amp))).T

    return cs_line, va_line


def get_flux(base_path, driver, period, post_amp, tube_r, exp_fac):

    data_dir = get_filepath(base_path, driver, period, post_amp, tube_r, exp_fac)

    path_join = partial(os.path.join, data_dir)

    if exp_fac:
        identifier = "%s_%s_%s_%s_%s"%(driver, period, post_amp, tube_r, exp_fac)
    else:
        identifier = "%s_%s_%s_%s"%(driver, period, post_amp, tube_r)

    Fpar_line = np.load(path_join("LineVar_{}_Fwpar.npy".format(identifier))).T
    Fperp_line = np.load(path_join("LineVar_{}_Fwperp.npy".format(identifier))).T
    Fphi_line = np.load(path_join("LineVar_{}_Fwphi.npy".format(identifier))).T

    Ftotal = np.sqrt(Fpar_line**2 + Fperp_line**2 + Fphi_line**2)

    Fpar_percent  = (Fpar_line / Ftotal)
    Fperp_percent = (Fperp_line / Ftotal)
    Fphi_percent  = (Fphi_line / Ftotal)

    #Filter out the noisy flux values before the wave starts propagating.
    filter_ftotal = (np.abs(Ftotal) <= 1e-5)
    Fpar_percent[filter_ftotal.nonzero()] = np.nan
    Fperp_percent[filter_ftotal.nonzero()] = np.nan
    Fphi_percent[filter_ftotal.nonzero()] = np.nan

    ParAvg = np.mean(Fpar_percent[np.isfinite(Fpar_percent)])
    PerpAvg = np.mean(Fperp_percent[np.isfinite(Fperp_percent)])
    PhiAvg = np.mean(Fphi_percent[np.isfinite(Fphi_percent)])

    beta_line = np.load(path_join("LineFlux_%s_%s_%s_beta.npy"%(driver,period,post_amp))).T
    return [Fpar_percent, Fperp_percent, Fphi_percent], beta_line, [ParAvg, PerpAvg, PhiAvg]


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


