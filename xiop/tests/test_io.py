import numpy as np
from xiop.qssa.io import load_qssa_bspline

from scipy.interpolate import BSpline

import pytest

def test_load_qssa_bspline():
    # Call the function
    bspline_p1, bspline_p2 = load_qssa_bspline()

    # Check the type of the returned objects
    assert isinstance(bspline_p1, BSpline)
    assert isinstance(bspline_p2, BSpline)