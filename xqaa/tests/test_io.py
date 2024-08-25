import numpy as np

from xqaa.qssa.io import load_qssa_bspline
from xqaa import params as xqaa_params

from scipy.interpolate import BSpline

import pytest

def test_load_qssa_bspline():
    xqaaParams = xqaa_params.XQAAParams()
    # Call the function
    bspline_p1, bspline_p2 = load_qssa_bspline(xqaaParams)

    # Check the type of the returned objects
    assert isinstance(bspline_p1, BSpline)
    assert isinstance(bspline_p2, BSpline)