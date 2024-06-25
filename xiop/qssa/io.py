""" I/O for QSSA items """
import os
from importlib.resources import files
import numpy as np
from scipy.interpolate import BSpline

def load_qssa_bspline():
    # File
    bspline_file = files('xiop').joinpath(
        os.path.join('data', 'qssa_bspline.npz'))

    # Load
    d = np.load(bspline_file)

    # Generate the BSplines
    bspline_p1 = BSpline(d['t_P1'], d['c_P1'], d['k_P1'])
    bspline_p2 = BSpline(d['t_P2'], d['c_P2'], d['k_P2'])

    # Return
    return bspline_p1, bspline_p2
    