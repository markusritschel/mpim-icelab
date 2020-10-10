#!/usr/bin/env python
# -*- coding utf-8 -*-
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2020-10-11
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import pytest


@pytest.fixture(scope="module")
def fixture(request):
    pass


@pytest.mark.skip(reason="no way of currently testing this")
def test_app(fixture):
    """Test based on the fixture"""
    assert fixture.title == str


def test_glob(global_fixture):
    """Test based on the fixture defined in contest.py"""
    assert global_fixture == 'Test'
