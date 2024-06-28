""" Figs for XIOP """
import os, sys
from importlib.resources import files

import numpy as np

from scipy.optimize import curve_fit
from scipy.stats import sigmaclip
import pandas


from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec
mpl.rcParams['font.family'] = 'stixgeneral'

import seaborn as sns

import corner

from oceancolor.utils import plotting 
from oceancolor.hydrolight import loisel23
from oceancolor.satellites import pace as sat_pace

from xiop.qssa import io as qio

# Local
#sys.path.append(os.path.abspath("../Analysis/py"))
#import anly_utils

from IPython import embed

def gen_cb(img, lbl, csz = 17.):
    cbaxes = plt.colorbar(img, pad=0., fraction=0.030)
    cbaxes.set_label(lbl, fontsize=csz)
    cbaxes.ax.tick_params(labelsize=csz)

def fig_qssa_coeffs(outroot='fig_qssa_coeffs', 
                    dataset:str='loisel23', 
                    extras={'X':1, 'Y':0}):
    """
    Generate a figure showing the QSSA coefficients derived from Loisel+2023.

    Parameters:
        outfile (str): The filename of the output figure (default: 'fig_u.png')

    """
    outfile = f'{outroot}_{dataset}.png'
    # Load
    data_file = qio.fits_filename(dataset, extras)
    d = np.load(data_file)

    bspline_h1, bspline_h2 = qio.load_qssa_bspline(
        dataset, extras)

    # Unpack
    wave = d['wave']
    H1 = d['ans'][:,0]
    H2 = d['ans'][:,1]
    rms = d['rms']

    waves = np.linspace(wave.min(), wave.max(), 1000)

    #
    bspclr = 'k'

    fig = plt.figure(figsize=(7,9))
    gs = gridspec.GridSpec(3,1)
    plt.clf()

    # ##############################################3
    # H1
    ax_h1 = plt.subplot(gs[0])
    ax_h1.plot(wave, H1, 'o')

    # Bspline
    ax_h1.plot(waves, bspline_h1(waves), '-', color=bspclr)

    # Label
    ax_h1.set_ylabel(r'$H_1$')
    ax_h1.tick_params(labelbottom=False)  # Hide x-axis labels


    # ##############################################3
    # H2
    ax_h2 = plt.subplot(gs[1])
    ax_h2.plot(wave, H2, 'o', color='g')

    # Bspline
    ax_h2.plot(waves, bspline_h2(waves), '-', color=bspclr)

    # Label
    ax_h2.set_ylabel(r'$H_2$')
    ax_h2.tick_params(labelbottom=False)  # Hide x-axis labels

    # RMS
    ax_rms = plt.subplot(gs[2])
    ax_rms.plot(wave, 100*rms, 'o', color='r')

    # Label
    ax_rms.set_xlabel('Wavelength (nm)')
    ax_rms.set_ylabel('Relative RMS (%)')

    for ax in [ax_h1, ax_h2, ax_rms]:
        plotting.set_fontsize(ax, 15.)
        ax.grid()
    
    #
    plt.tight_layout()#pad=0.0, h_pad=0.0, w_pad=0.3)
    plt.savefig(outfile, dpi=300)
    print(f"Saved: {outfile}")


def main(flg):
    if flg== 'all':
        flg= np.sum(np.array([2 ** ii for ii in range(25)]))
    else:
        flg= int(flg)

    # Spectra
    if flg == 1:
        fig_qssa_coeffs()#, bbscl=20)

# Command line execution
if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        flg = 0

        #flg = 1
        
    else:
        flg = sys.argv[1]

    main(flg)
