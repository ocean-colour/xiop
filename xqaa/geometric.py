""" Geometric considerations """

import numpy as np

def rrs_from_Rrs(Rrs:np.ndarray):

    # Lee+2002
    A, B = 0.52, 1.17

    # Calculate
    rrs = Rrs / (A + B*Rrs)

    # Return
    return rrs