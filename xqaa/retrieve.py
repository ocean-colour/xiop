""" Methods for the XQAA retrieval """
import warnings

import numpy as np
from scipy.interpolate import interp1d

from ocpy.water import absorption
from ocpy.hydrolight import loisel23

from xqaa.params import XQAAParams
from xqaa import geometric as xqaa_geom
from xqaa import inversion

from IPython import embed

def iops_from_Rrs(wave:np.ndarray, Rrs:np.ndarray, 
                  xparams:XQAAParams):
    """
    Calculate the IOPs from the remote sensing reflectance.

    Parameters:
        wave (np.ndarray): Array of wavelengths.
        Rrs (np.ndarray): Array of remote sensing reflectance values.
        xparams (XQAAParams): XQAA parameters.

    Returns:
        tuple: A tuple containing the absorption and backscatter values.
    """

    # Water
    aw = absorption.a_water(wave)

    warnings.warn("Need to implement b_w")
    l23_ds = loisel23.load_ds(4,0)
    l23_bbw = (l23_ds.bb.data - l23_ds.bbnw.data)[0]
    f = interp1d(l23_ds.Lambda.data, l23_bbw, kind='linear')
                    #bounds_error=False, fill_value='extrapolate')
    bbw = f(wave)

    # rrs
    rrs = xqaa_geom.rrs_from_Rrs(Rrs)

    # Gordon Coefficients
    G1, G2 = inversion.calc_Gcoeff(wave, xparams)
    D = inversion.quadratic(rrs, G1, G2)

    # bbnw
    bbnw = inversion.retrieve_bbnw(aw, bbw, D)
    avgbb_wvs = (wave > xparams.bbmin) & (wave < xparams.bbmax)

    # Find the correction to use for anw
    avg_bbnw = np.nanmean(bbnw[avgbb_wvs])
    if xparams.bbnw_corr == 'mean':
        corr_bbnw = avg_bbnw
    elif xparams.bbnw_corr == 'pow':
        corr_bbnw = avg_bbnw*(wave/np.mean(wave[avgbb_wvs]))**(-1)
        #embed(header='iops_from_Rrs 70')
    elif xparams.bbnw_corr == 'none':
        corr_bbnw = 0.
    else:
        raise ValueError(f"Bad bbnw_corr: {xparams.bbnw_corr}")

    # anw
    anw = inversion.retrieve_anw(aw, bbw, D, 
                                 corr_bbnw=corr_bbnw)

    # Return
    return anw, corr_bbnw, avg_bbnw