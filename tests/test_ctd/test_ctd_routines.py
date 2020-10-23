# !/usr/bin/env python
# -*- coding utf-8 -*-
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  kontakt@markusritschel.de
# Date:   11/10/2020
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import pathlib
import pytest
import xarray

from mpim_icelab.ctd import read_ctd


SBE_TESTFILE = pathlib.Path(__file__).parent / 'data/sbe37sm-example-data.cnv'
SBE_TESTLOG  = pathlib.Path(__file__).parent / 'data/sbe37sm-example-log.dat'
RBR_TESTFILE = pathlib.Path(__file__).parent / 'data/rbr-example-data.dat'

@pytest.fixture
def seabird_ctd_ds():
    return read_ctd(SBE_TESTFILE)


@pytest.fixture
def seabird_log_ds():
    return read_ctd(SBE_TESTLOG)


@pytest.fixture
def rbr_ctd_ds():
    return read_ctd(RBR_TESTFILE)


def test_seabird(seabird_ctd_ds, seabird_log_ds):
    assert isinstance(seabird_ctd_ds, xarray.Dataset)
    assert isinstance(seabird_log_ds, xarray.Dataset)


def test_rbr(rbr_ctd_ds):
    assert isinstance(rbr_ctd_ds, xarray.Dataset)


@pytest.mark.parametrize("file", [SBE_TESTFILE, SBE_TESTLOG, RBR_TESTFILE])
def test_read_ctd(file):
    ds = read_ctd(file)
    assert isinstance(ds, xarray.Dataset)
