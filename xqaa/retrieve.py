""" Methods for the XQAA retrieval """

import numpy as np

from xqaa import geometric as xqaa_geom
from xqaa import inversion

def iops_from_Rrs(wave:np.ndarray, Rrs:np.ndarray, params:dict):
    """
    Calculate the IOPs from the remote sensing reflectance.

    Parameters:
        wave (np.ndarray): Array of wavelengths.
        Rrs (np.ndarray): Array of remote sensing reflectance values.
        params (dict): Dictionary of parameters.

    Returns:
        tuple: A tuple containing the absorption and backscatter values.
    """

    # rrs
    rrs = xqaa_geom.rrs_from_Rrs(Rrs)

    # Coefficients
    H1, H2 = inversion.calc_Hcoeff(wave, params)
    D = inversion.quadratic(rrs, H1, H2)