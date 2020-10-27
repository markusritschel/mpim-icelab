# !/usr/bin/env python
# -*- coding utf-8 -*-
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  kontakt@markusritschel.de
# Date:   11/10/2020
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import numpy
import pathlib
import pytest
import xarray
from mpim_icelab.harps import read_salinity_harps
from mpim_icelab.harps.salinity_harps import calc_brine_salinity, calc_freezing_starts

# base_dir = os.path.dirname(os.path.abspath(__file__))
# pathlib.Path.cwd()
# all_files = glob.glob(os.path.join(base_dir, '*.log'))

TESTFILE = pathlib.Path(__file__).parent / 'salinity_harps_test_data.dat'

@pytest.fixture
def harp_dataset(file=TESTFILE):
    return read_salinity_harps(file)


def test_salinity(harp_dataset):
    assert isinstance(harp_dataset, xarray.Dataset)
    assert harp_dataset.coords['time'].dtype == 'datetime64[ns]'


@pytest.mark.parametrize("method", ['Assur', 'N&W09', 'Vancoppenolle'])
def test_calc_brine_salinity(harp_dataset, method):
    T = numpy.random.random(10)
    S_brine = calc_brine_salinity(T, method=method)
    assert isinstance(S_brine, numpy.ndarray)
    assert len(T) == len(S_brine)


@pytest.mark.parametrize("method", ['median', 'savgol'])
def test_calc_freezing_starts(harp_dataset, method):
    freezing_starts = calc_freezing_starts(harp_dataset, 'r16', kind=method, tolerance=1e-4)
    assert isinstance(freezing_starts, xarray.DataArray)
    assert freezing_starts.size == harp_dataset.wire_pair.size * harp_dataset.module.size
    assert freezing_starts.shape == (harp_dataset.module.size, harp_dataset.wire_pair.size)


def test_calc_ice_properties(harp_dataset):
    data = harp_dataset.copy().seaice.calc_ice_properties()
    assert isinstance(data, xarray.Dataset)
    for var in ['temperature', 'brine_salinity', 'liquid_fraction', 'solid_fraction']:
        assert var in data.data_vars, "{} not found in dataset after calculating ice properties".format(var)
        assert hasattr(data[var], 'units')


@pytest.mark.skip(reason="no way of currently testing this")
def test_computed_quantities(harp_dataset):
    for var in ['brine salinity', 'solid fraction', 'liquid fraction', 'bulk salinity']:
        assert var in harp_dataset.data_vars


@pytest.mark.skip(reason="no way of currently testing this")
def test_reference_resistance(harp_dataset):
    resistance = harp_dataset['r16']
    freezing_onset = harp_dataset['freezing_start']
    assert isinstance(resistance, xarray.DataArray)
    assert resistance['wire_harps'].size == freezing_onset


@pytest.mark.skip(reason="no way of currently testing this")
def test_solid_liquid_fraction(harp_dataset):
    assert numpy.all((harp_dataset.liquid_fraction + harp_dataset.solid_fraction).dropna('time') == 1), \
        'Liquid and solid fraction should match up to 1.'
