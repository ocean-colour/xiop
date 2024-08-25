""" Tests for retrieve module. """
import numpy as np
import pandas

from xqaa import params as xqaa_params
from xqaa import retrieve

from scipy.interpolate import BSpline

import pytest

def test_iop_from_Rrs():
    """ Test the load_params function.
    """
    xqaaParams = xqaa_params.XQAAParams()

    # Create some dummy data
    df = pandas.read_csv('files/test_Rrs.csv')

    # Call the function
    anw, bbnw = retrieve.iops_from_Rrs(
        df.wave.values, df.Rrs.values, xqaaParams)

    # Check the values
    #pytest.set_trace()
    assert np.isclose(anw[-1], 0.361059, atol=1e-5)
    assert np.isclose(bbnw[-1], 0.000549, atol=1e-5)

'''
from ocpy.hydrolight import loisel23
import pandas

# Load 
l23_ds = loisel23.load_ds(4,0)

# Unpack
l23_wave = l23_ds.Lambda.data
l23_Rrs = l23_ds.Rrs.data

# Grab one
Rrs = l23_Rrs[0]

# Write
df = pandas.DataFrame({'wave':l23_wave, 'Rrs':Rrs})
df.to_csv('files/test_Rrs.csv', index=False)
print('Wrote files/test_Rrs.csv')
'''

