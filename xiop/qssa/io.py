""" I/O for QSSA items """
import os
from importlib.resources import files
import numpy as np
from scipy.interpolate import BSpline

def fits_filename(dataset:str, extras:dict):

    if dataset == 'loisel23':
        exs = f'_X{extras["X"]}Y{extras["Y"]}'
    else:
        exs = ''

    base = f'qssa_fits_{dataset}{exs}.npz'
    filename = files('xiop').joinpath(
        os.path.join('data', base))

    # Return
    return filename

def bspline_filename(dataset:str, extras:dict):

    if dataset == 'loisel23':
        exs = f'_X{extras["X"]}Y{extras["Y"]}'
    else:
        exs = ''

    base = f'qssa_bspline_{dataset}{exs}.npz'
    filename = files('xiop').joinpath(
        os.path.join('data', base))

    # Return
    return filename
    
def load_qssa_bspline():
    """
    Load the QSSA B-spline data from a file and generate the corresponding B-spline objects.

    Returns:
        tuple: A tuple containing two B-spline objects, bspline_p1 and bspline_p2.
    """
    # File
    bspline_file = files('xiop').joinpath(
        os.path.join('data', 'qssa_bspline.npz'))

    # Load
    d = np.load(bspline_file)

    # Generate the BSplines
    bspline_p1 = BSpline(d['t_H1'], d['c_H1'], d['k_H1'])
    bspline_p2 = BSpline(d['t_H2'], d['c_H2'], d['k_H2'])

    # Return
    return bspline_p1, bspline_p2
    