""" Development of XQAA methods """
import numpy as np

import seaborn as sns
from matplotlib import pyplot as plt

from ocpy.hydrolight import loisel23
from ocpy.utils import plotting

from bing import rt

from xqaa import geometric as xqaa_geom
from xqaa import inversion

def prepl23_for_sensitivity(extras:dict, idx:int):
    l23_ds = loisel23.load_ds(extras['X'],
                              extras['Y'])

    # Unpack
    l23_wave = l23_ds.Lambda.data
    l23_Rrs = l23_ds.Rrs.data
    l23_bbnw = l23_ds.bbnw.data

    # Water
    aw = (l23_ds.a.data - l23_ds.anw.data)[0]
    bbw = (l23_ds.bb.data - l23_ds.bbnw.data)[0]

    # More
    Rrs_true = l23_Rrs[idx]
    bbnw_true = l23_bbnw[idx]
    rrs_true = xqaa_geom.rrs_from_Rrs(Rrs_true)

    # Rrs
    Rrs = rt.calc_Rrs(l23_ds.a.data[idx], 
                      l23_ds.bb.data[idx])
    rrs = xqaa_geom.rrs_from_Rrs(Rrs)
    return l23_wave, rrs, aw, bbw, bbnw_true

def sensitivity_to_G1(dataset:str='loisel23', 
                extras = {'X':1, 'Y':0},
                idx:int=170, outroot:str='sens_G1'):
    outfile = f'{outroot}_{dataset}.png'
    dG1s = [-0.002, -0.001, 0., 0.001, 0.002]
 
    l23_wave, rrs, aw, bbw, bbnw_true = prepl23_for_sensitivity(
        extras, idx)

    # Do it
    all_diffs = []
    all_rdiffs = []
    for dG1 in dG1s:
        G1 = rt.G1 + dG1
        D = inversion.quadratic(rrs, G1, rt.G2)
        bbnw = inversion.retrieve_bbnw(aw, bbw, D)

        # Difference
        diff = bbnw - bbnw_true
        rdiff = diff / bbnw_true
        all_diffs.append(diff)
        all_rdiffs.append(rdiff)

    # Plot me
    fig_sens(l23_wave, all_rdiffs, 'G_1', dG1s, outfile)


def sensitivity_to_G2(dataset:str='loisel23', 
                extras = {'X':1, 'Y':0},
                idx:int=170, outroot:str='sens_G2'):
    outfile = f'{outroot}_{dataset}.png'
    dG2s = [0.80, 0.90, 1., 1.1, 1.2]
 
    l23_wave, rrs, aw, bbw, bbnw_true = prepl23_for_sensitivity(
        extras, idx)

    # Do it
    all_diffs = []
    all_rdiffs = []
    for dG2 in dG2s:
        G2 = rt.G2*dG2
        D = inversion.quadratic(rrs, rt.G1, G2)
        bbnw = inversion.retrieve_bbnw(aw, bbw, D)

        # Difference
        diff = bbnw - bbnw_true
        rdiff = diff / bbnw_true
        all_diffs.append(diff)
        all_rdiffs.append(rdiff)

    # Plot me
    fig_sens(l23_wave, all_rdiffs, 'G_2', dG2s, outfile)

def fig_sens(wave:np.ndarray, all_rdiffs:list, 
             var:str, vals:list, outfile:str):

    # Plot me
    fig = plt.figure(figsize=(9,6))
    ax = plt.gca()

    for ss, rdiff in enumerate(all_rdiffs):
        ax.plot(wave, 100*rdiff, 
                label=r'$\delta '+f'{var}'+'='+f'{vals[ss]}'+r'$')
        
    #
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel(r'$\delta b_{b,nw}/b_{b,nw}$'+'  [%]')
    # 
    ax.axhline(0.0, color='k', linestyle='--')
    ax.grid()

    ax.set_ylim(-20., 20.)
    ax.set_xlim(550., None)
    #
    ax.legend(fontsize=15.)
    plotting.set_fontsize(ax, 17)
    #
    plt.tight_layout()
    plt.savefig(outfile, dpi=300)
    print(f"Saved: {outfile}")


if __name__ == '__main__':

    sensitivity_to_G1()
    sensitivity_to_G2()