""" Tests for the functions in the params module. """
import numpy as np
from xqaa import params as xqaa_params

from scipy.interpolate import BSpline

import pytest

def test_load_params():
    """ Test the load_params function.
    """
    xqaaParams = xqaa_params.XQAAParams()