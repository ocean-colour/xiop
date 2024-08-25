""" I/O for QSSA items """
import os
from importlib.resources import files
import numpy as np
from scipy.interpolate import BSpline

from xqaa import params as xqaa_params

def fits_filename(dataset:str, extras:dict):
    """
    Generate a filename for a FITS dataset.

    Args:
        dataset (str): The name of the dataset.
        extras (dict): A dictionary containing extra parameters.

    Returns:
        str: The generated filename for the FITS dataset.
    """

    if dataset == 'loisel23':
        exs = f'_X{extras["X"]}Y{extras["Y"]}'
    else:
        exs = ''

    base = f'qssa_fits_{dataset}{exs}.npz'
    filename = files('xqaa').joinpath(
        os.path.join('data', base))

    # Return
    return filename

def bspline_filename(params:xqaa_params.XQAAParams):
    """
    Generate the filename for the B-spline dataset.

    Parameters:
        params (XQAAParams): The parameters for the XQAA model.

    Returns:
        filename (str): The generated filename for the B-spline dataset.
    """

    if params.dataset == 'loisel23':
        exs = f'_X{params.L23_X}Y{params.L23_Y}'
    else:
        exs = ''

    base = f'qssa_bspline_{params.dataset}{exs}.npz'
    filename = files('xqaa').joinpath(
        os.path.join('data', base))

    # Return
    return filename
    
def load_qssa_bspline(params:xqaa_params.XQAAParams):
    """
    Load the QSSA B-spline data from a file and generate the corresponding B-spline objects.

    Parameters:
        params (XQAAParams): The parameters for the XQAA model.

    Returns:
        tuple: A tuple containing two B-spline objects, bspline_p1 and bspline_p2.
    """
    # File
    bspline_file = bspline_filename(params)

    # Load
    d = np.load(bspline_file)

    # Generate the BSplines
    bspline_p1 = BSpline(d['t_H1'], d['c_H1'], d['k_H1'])
    bspline_p2 = BSpline(d['t_H2'], d['c_H2'], d['k_H2'])

    # Return
    return bspline_p1, bspline_p2
    