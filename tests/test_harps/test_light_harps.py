# !/usr/bin/env python
# -*- coding utf-8 -*-
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  kontakt@markusritschel.de
# Date:   25/10/2020
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import pathlib
import pytest
import xarray

from mpim_icelab.harps import read_light_harp


TESTFILE_dirty = pathlib.Path(__file__).parent / 'light_harps_test_data_dirty.txt'
TESTFILE_clean = pathlib.Path(__file__).parent / 'light_harps_test_data_clean.txt'


@pytest.fixture
def harp_dataset(file=TESTFILE_clean):
    with pytest.raises(ValueError):
        read_light_harp(TESTFILE_dirty)
    return read_light_harp(file)


def test_read_light_harp(harp_dataset):
    assert isinstance(harp_dataset, xarray.Dataset)
