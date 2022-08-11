# !/usr/bin/env python
# -*- coding utf-8 -*-
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  kontakt@markusritschel.de
# Date:   23/10/2020
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import pathlib
import pytest
import xarray

from mpim_icelab.tsticks import read_tsticks


TESTFILE_dirty = pathlib.Path(__file__).parent / 'tstick_data_dirty.dat'
TESTFILE_clean = pathlib.Path(__file__).parent / 'tstick_data_clean.dat'
TESTFILE_clean = pathlib.Path(__file__).parent / 'tstick_data_new_format.log'


@pytest.fixture
def tsticks_dataset(file=TESTFILE_clean):
    # with pytest.raises(ValueError):
    #     read_tsticks(TESTFILE_dirty)
    return read_tsticks(file)


def test_read_tstick(tsticks_dataset):
    assert isinstance(tsticks_dataset, xarray.Dataset)
