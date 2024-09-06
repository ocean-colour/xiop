""" Perform analysis on Loisel et al. 2023 data. """

import numpy as np

from matplotlib import pyplot as plt

from ocpy.hydrolight import loisel23
from ocpy.utils import plotting

from xqaa import geometric as xiop_geom
from xqaa import inversion
from xqaa import params as xqaa_params

from IPython import embed

def stats(dataset:str='loisel23', extras:dict={'X':1, 'Y':0}, 
          bbnw_corr:str='none'):

    # Parameters
    xqaaParams = xqaa_params.XQAAParams()
    xqaaParams.L23_X = extras['X']
    xqaaParams.L23_Y = extras['Y']

    outfile = f'stats_{dataset}_{bbnw_corr}.png'

    # Load
    l23_ds = loisel23.load_ds(extras['X'], extras['Y'])

    # Unpack
    l23_wave = l23_ds.Lambda.data
    l23_Rrs = l23_ds.Rrs.data
    l23_anw = l23_ds.anw.data    
    l23_bbnw = l23_ds.bbnw.data    

    
    a_wvs = (l23_wave > 400.) & (l23_wave < 450.)
    bb_wvs = l23_wave > 600.
    avgbb_wvs = (l23_wave > 600.) & (l23_wave < 650.)

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
        G1, G2 = inversion.calc_Gcoeff(l23_wave, xqaaParams)
        D = inversion.quadratic(rrs, G1, G2)

        bbnw = inversion.retrieve_bbnw(aw, bbw, D)
        if bbnw_corr == 'mean':
            corr_bbnw = np.nanmean(bbnw[avgbb_wvs])
        elif 'pow' in bbnw_corr: 
            exp = float(bbnw_corr[3:])
            avgbbnw = np.nanmean(bbnw[avgbb_wvs])
            corr_bbnw = avgbbnw*(l23_wave/np.mean(l23_wave[avgbb_wvs]))**(exp)
        elif bbnw_corr == 'none':
            corr_bbnw = 0.
        else:
            raise ValueError(f"Bad bbnw_corr: {bbnw_corr}")

        #embed(header='47 of loisel23.py: stats()')
        # anw
        anw = inversion.retrieve_anw(aw, bbw, D, 
                                     corr_bbnw=corr_bbnw)

        # Stats
        roff_a.append( np.nanmedian(((anw - anw_true)/anw_true)[a_wvs]))
        roff_bb.append( np.nanmedian(((bbnw - bbnw_true)/bbnw_true)[bb_wvs]))
    roff_a = np.array(roff_a)
    roff_bb = np.array(roff_bb)

    # More stats
    rms_a = np.sqrt(np.mean(roff_a**2))
    rms_bb = np.sqrt(np.mean(roff_bb**2))

    # Shwo simple histograms of each of these
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].hist(100*roff_a, bins=50, color='b', alpha=0.5)
    axs[0].set_title('anw: 400-450nm')
    axs[1].hist(100*roff_bb, bins=50, color='r', alpha=0.5)
    axs[1].set_title('bbnw: 600-750nm')
    # Text
    axs[0].text(0.95, 0.9, f'bbnw corr: {bbnw_corr}', 
                transform=axs[0].transAxes, fontsize=15,
                ha='right')
    # RMS text
    axs[0].text(0.95, 0.8, f'RMS: {100*rms_a:.2f}%', 
                transform=axs[0].transAxes, fontsize=15,
                ha='right')
    axs[1].text(0.95, 0.8, f'RMS: {100*rms_bb:.2f}%', 
                transform=axs[1].transAxes, fontsize=15,
                ha='right')
                
    # Label
    axs[0].set_xlabel(r'$a_{\rm nw}$: Relative Offset [%]')
    axs[1].set_xlabel(r'$b_{\rm b,nw}$: Relative Offset [%]')
    for ax in axs:
        ax.set_ylabel('Count')
        # Add a vertical line
        ax.axvline(0, color='k', linestyle='--')
        plotting.set_fontsize(ax, 15.)
    
    plt.tight_layout()
    plt.savefig(outfile, dpi=300)
    print(f'Saved: {outfile}')

    #embed(header='54 of loisel23.py: stats()')

if __name__ == '__main__':

    # bbnw
    #stats()
    #stats(bbnw_corr='mean')
    stats(bbnw_corr='pow-1')
    stats(bbnw_corr='pow-2')