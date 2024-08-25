""" Tests for retrieve module. """
import numpy as np

from xqaa import params as xqaa_params
from xqaa import retrieve

from scipy.interpolate import BSpline

import pytest

def test_iop_from_Rrs():
    """ Test the load_params function.
    """
    xqaaParams = xqaa_params.XQAAParams()

    # Create some dummy data
    wave = np.arange(400, 750, 1.)
    Rrs = np.ones_like(wave)*1e-3

