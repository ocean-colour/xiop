""" Methods for the XQAA retrieval """

import numpy as np
import warnings

from ocpy.water import absorption
from ocpy.hydrolight import loisel23

from xqaa.params import XQAAParams
from xqaa import geometric as xqaa_geom
from xqaa import inversion

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
    bbw = (l23_ds.bb.data - l23_ds.bbnw.data)[0]

    # rrs
    rrs = xqaa_geom.rrs_from_Rrs(Rrs)

    # Gordon Coefficients
    H1, H2 = inversion.calc_Hcoeff(wave, xparams)
    D = inversion.quadratic(rrs, H1, H2)

    # bbnw
    bbnw = inversion.retrieve_bbnw(aw, bbw, D)
    avgbb_wvs = (wave > xparams.bbmin) & (wave < xparams.bbmax)

    # Find the correction to use for anw
    if xparams.bbnw_corr == 'mean':
        corr_bbnw = np.nanmean(bbnw[avgbb_wvs])
    elif xparams.bbnw_corr == 'pow':
        avgbbnw = np.nanmean(bbnw[avgbb_wvs])
        corr_bbnw = avgbbnw*(wave/np.mean(wave[avgbb_wvs]))**(-1)
    elif xparams.bbnw_corr == 'none':
        corr_bbnw = 0.
    else:
        raise ValueError(f"Bad bbnw_corr: {xparams.bbnw_corr}")

    # anw
    anw = inversion.retrieve_anw(aw, bbw, D, 
                                 corr_bbnw=corr_bbnw)

    # Return
    return anw, bbnw