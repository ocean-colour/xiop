""" Figs for XIOP """
import os, sys

import numpy as np

from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec
mpl.rcParams['font.family'] = 'stixgeneral'


from ocpy.utils import plotting 

from xqaa.qssa import io as qio
from xqaa import params as xqaa_params

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
                    extras={'X':1, 'Y':0},
                    layout='vertical'):
    """
    Generate a figure showing the QSSA coefficients derived from Loisel+2023.

    Parameters:
        outfile (str): The filename of the output figure (default: 'fig_u.png')

    """
    # Parameters
    if dataset != 'loisel23':
        raise ValueError("Only Loisel23 dataset is supported") 
    xqaaParams = xqaa_params.XQAAParams()
    xqaaParams.L23_X = extras['X']
    xqaaParams.L23_Y = extras['Y']


    outfile = f'{outroot}_{dataset}.png'
    # Load
    data_file = qio.fits_filename(xqaaParams)
    d = np.load(data_file)

    bspline_g1, bspline_g2 = qio.load_qssa_bspline(xqaaParams)

    # Unpack
    wave = d['wave']
    G1 = d['ans'][:,0]
    G2 = d['ans'][:,1]
    rms = d['rms']

    waves = np.linspace(wave.min(), wave.max(), 1000)

    #
    bspclr = 'k'

    if layout == 'horizontal':
        fig = plt.figure(figsize=(12,4))
        gs = gridspec.GridSpec(1,3)
    else:
        fig = plt.figure(figsize=(7,9))
        gs = gridspec.GridSpec(3,1)
    plt.clf()

    # ##############################################3
    # G1
    ax_g1 = plt.subplot(gs[0])
    ax_g1.plot(wave, G1, 'o')

    # Bspline
    ax_g1.plot(waves, bspline_g1(waves), '-', color=bspclr)

    # Label
    ax_g1.set_ylabel(r'$G_1$')
    if layout == 'vertical':
        ax_g1.tick_params(labelbottom=False)  # Hide x-axis labels


    # ##############################################3
    # G2
    ax_g2 = plt.subplot(gs[1])
    ax_g2.plot(wave, G2, 'o', color='g')

    # Bspline
    ax_g2.plot(waves, bspline_g2(waves), '-', color=bspclr)

    # Label
    ax_g2.set_ylabel(r'$G_2$')
    if layout == 'vertical':
        ax_g2.tick_params(labelbottom=False)  # Hide x-axis labels

    # RMS
    ax_rms = plt.subplot(gs[2])
    ax_rms.plot(wave, 100*rms, 'o', color='r')

    # Label
    ax_rms.set_ylabel('Relative RMS (%)')

    for ax in [ax_g1, ax_g2, ax_rms]:
        plotting.set_fontsize(ax, 15.)
        ax.grid()
        if layout == 'horizontal' or ax == ax_rms:
            ax.set_xlabel('Wavelength (nm)')
    
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
        #fig_qssa_coeffs()#, bbscl=20)
        fig_qssa_coeffs(layout='horizontal')#, bbscl=20)

# Command line execution
if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        flg = 0

        #flg = 1
        
    else:
        flg = sys.argv[1]

    main(flg)
