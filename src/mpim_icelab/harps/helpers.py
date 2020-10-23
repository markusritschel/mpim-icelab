#!/usr/bin/env python
# -*- coding utf-8 -*-
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  kontakt@markusritschel.de
# Date:   06/03/2019
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
from __future__ import division, print_function, absolute_import

import numpy as np
from scipy import signal
import xarray as xr


def savgol(obj, axis=0):
    """Helper function to apply a Savitzky-Golay filter to an xarray object."""
    func = lambda x: signal.savgol_filter(x, 1001, 2, mode='nearest', axis=axis)
    return xr.apply_ufunc(func, obj)


def butterworth(obj, axis=0):
    """Helper function to apply a Butterworth filter to an xarray object."""
    b, a = signal.butter(3, .002, output='ba')
    func = lambda x: signal.filtfilt(b, a, x, axis=axis)
    return xr.apply_ufunc(func, obj)


def median(obj, time=200):
    """Helper function to apply a median filter to an xarray object."""
    return obj.rolling(time=time, center=True).median()


def grad(obj, dist=2, axis=0):
    """Helper function to apply a gradient to an xarray object."""
    obj = obj
    func = lambda x: np.gradient(x, dist, axis=axis)
    return xr.apply_ufunc(func, obj)
