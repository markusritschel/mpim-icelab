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


@pytest.fixture()
def global_fixture(request):
    return 'Test'
