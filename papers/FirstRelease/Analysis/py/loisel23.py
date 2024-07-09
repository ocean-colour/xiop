""" Perform analysis on Loisel et al. 2023 data. """

import numpy as np

from matplotlib import pyplot as plt

from ocpy.hydrolight import loisel23
from ocpy.utils import plotting

from xiop import geometric as xiop_geom
from xiop import inversion

from IPython import embed

def stats(extras={'X':1, 'Y':0}):

    # Load
    dataset = 'loisel23'
    l23_ds = loisel23.load_ds(extras['X'], extras['Y'])

    # Unpack
    l23_wave = l23_ds.Lambda.data
    l23_Rrs = l23_ds.Rrs.data
    l23_anw = l23_ds.anw.data    
    l23_bbnw = l23_ds.bbnw.data    

    
    a_wvs = (l23_wave > 400.) & (l23_wave < 450.)
    bb_wvs = l23_wave > 600.

    # Water
    aw = (l23_ds.a.data - l23_ds.anw.data)[0]
    bbw = (l23_ds.bb.data - l23_ds.bbnw.data)[0]


    # Loop me
    roff_a = []
    roff_bb = []

    for idx in range(l23_Rrs.shape[0]):
        # 
        Rrs = l23_Rrs[idx]
        bbnw_true = l23_bbnw[idx]
        anw_true = l23_anw[idx]

        # rrs
        rrs = xiop_geom.rrs_from_Rrs(Rrs)

        # Coefficients
        H1, H2 = inversion.calc_Hcoeff(l23_wave, dataset, extras)
        D = inversion.quadratic(rrs, H1, H2)

        bbnw = inversion.retrieve_bbnw(aw, bbw, D)
        anw = inversion.retrieve_anw(aw, bbw, D)

        # Stats
        roff_a.append( np.nanmedian(((anw - anw_true)/anw_true)[a_wvs]))
        roff_bb.append( np.nanmedian(((bbnw - bbnw_true)/bbnw_true)[bb_wvs]))
    roff_a = np.array(roff_a)
    roff_bb = np.array(roff_bb)


    # Shwo simple histograms of each of these
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].hist(100*roff_a, bins=50, color='b', alpha=0.5)
    axs[0].set_title('anw')
    axs[1].hist(100*roff_bb, bins=50, color='r', alpha=0.5)
    axs[1].set_title('bbnw')
    # Label
    axs[0].set_xlabel(r'$a_{\rm nw}$: Relative Offset [%]')
    axs[1].set_xlabel(r'$b_{\rm b,nw}$: Relative Offset [%]')
    for ax in axs:
        ax.set_ylabel('Count')
        # Add a vertical line
        ax.axvline(0, color='k', linestyle='--')
        plotting.set_fontsize(ax, 15.)
    
    outfile = f'stats_{dataset}.png'
    plt.tight_layout()
    plt.savefig(outfile, dpi=300)
    print(f'Saved: {outfile}')

    #embed(header='54 of loisel23.py: stats()')

if __name__ == '__main__':

    # bbnw
    stats()