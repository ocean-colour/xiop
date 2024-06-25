""" Derive the coefficients for the QSSA """

import numpy as np
import os
from importlib.resources import files

from scipy.optimize import curve_fit
from scipy.interpolate import BSpline
from scipy.interpolate import make_interp_spline



from oceancolor.hydrolight import loisel23

from IPython import embed

def rrs_func(uval:np.ndarray, G1:float, G2:float):
    rrs = G1*uval + G2*uval**2
    return rrs

def fit_loisel23(outfile:str=None, X:int=4, Y:int=0, dw:int=1):

    if outfile is None:
        outfile = files('xiop').joinpath(
            os.path.join('data', 'qssa_fits.npz'))

    # Load Loisel+2023
    l23_ds = loisel23.load_ds(X,Y)

    # Unpack
    l23_Rrs = l23_ds.Rrs.data
    l23_wave = l23_ds.Lambda.data
    a = l23_ds.a.data
    bb = l23_ds.bb.data

    # u
    u = bb / (a+bb)

    # rrs
    A, B = 0.52, 1.17  # Lee+2002
    rrs = l23_Rrs / (A + B*l23_Rrs)

    # Loop on every 3 points + the last
    save_ans = []
    save_cov = []
    waves = []
    save_rms = []
    for ss in range(0, l23_wave.size, dw):

        # Derive the coefficients
        ans, cov = curve_fit(rrs_func, u[:,ss], rrs[:,ss], 
                             p0=[0.1, 0.1]) #sigma=np.ones_like(u[:,ii])*0.0003)
        # RMS
        irrs = rrs_func(u[:,ss], ans[0], ans[1])
        rms = np.sqrt(np.mean((rrs[:,ss] - irrs)**2/(irrs**2)))

        # Save
        save_ans.append(ans)                            
        save_cov.append(cov)
        waves.append(l23_wave[ss])
        save_rms.append(rms)

        # Print
        print(f"wave={l23_wave[ss]}, ans={ans}, rms={100*rms}%")#cov={np.sqrt(np.diag(cov))}")

    # Save
    np.savez(outfile, ans=save_ans, cov=save_cov, wave=waves, rms=save_rms)
    print(f'Saved to {outfile}')
    
    return np.array(waves), np.array(save_ans), np.array(save_cov)

def spline_me():
    # Load
    data_file = files('xiop').joinpath(
        os.path.join('data', 'qssa_fits.npz'))
    d = np.load(data_file)

    # Unpack
    wave = d['wave']
    P1 = d['ans'][:,0]
    P2 = d['ans'][:,1]

    # Splines
    bspline_p1 = make_interp_spline(wave, P1)
    bspline_p2 = make_interp_spline(wave, P2)

    # Save
    outfile = files('xiop').joinpath(
        os.path.join('data', 'qssa_bspline.npz'))

    # Save the coefficients to a NumPy archive
    #embed(header='Breakpoint 92')
    np.savez(outfile, t_P1=bspline_p1.t, c_P1=bspline_p1.c, k_P1=bspline_p1.k,
                    t_P2=bspline_p2.t, c_P2=bspline_p2.c, k_P2=bspline_p2.k) 
    print(f'Saved to {outfile}')

if __name__ == '__main__':

    # Fit em
    #fit_loisel23()

    # Spline em
    spline_me()