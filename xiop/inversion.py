""" Algorithms related to the Inversion """
import numpy as np

from xiop.qssa.io import load_qssa_bspline

def find_lambdab(wave:np.ndarray, rrs:np.ndarray):

    return 440. # nm

def find_lambdar(wave:np.ndarray, rrs:np.ndarray):

    return 550. # nm
            
def calc_Hcoeff(wave:np.ndarray, dataset:str, extras:dict):
    # Load the Bsplines
    bspline_p1, bspline_p2 = load_qssa_bspline(dataset, extras)
    
    # Evaulate the coefficients
    H1 = bspline_p1(wave)
    H2 = bspline_p2(wave)

    return H1, H2


def quadratic(rrs:np.ndarray, 
              H1:np.ndarray, H2:np.ndarray):
    """
    Perform quadratic inversion to calculate the D value.

    rrs = H1*u + H2*u^2

        a = H2
        b = H1
        c = -rrs

    u = (-b + sqrt(b^2 - 4ac))/(2a)

    Parameters:
        wave (np.ndarray): Array of wavelengths.
        rrs (np.ndarray): Array of remote sensing reflectance values.
        H1 (np.ndarray): Array of H1 values.
        H2 (np.ndarray): Array of H2 values.

    Returns:
        D (np.ndarray): Array of calculated D values.
    """

    # Quadratic equation
    sq = np.sqrt(H1**2 + 4*H2*rrs)
    upos = (-1*H1 + sq)/(2*H2)

    # Query for positive values
    bad = upos < 0
    if np.any(bad):
        raise ValueError(f"Negative values in quadratic inversion")

    # Use D
    D = 1/upos - 1

    # Return
    return D

def retrieve_anw(aw:np.ndarray, bbw:np.ndarray, D:np.ndarray):

    anw = D*bbw - aw

    return anw

def retrieve_bbnw(aw:np.ndarray, bbw:np.ndarray, D:np.ndarray):

    bbnw = aw/D - bbw

    return bbnw