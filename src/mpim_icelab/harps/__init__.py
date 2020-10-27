# !/usr/bin/env python
# -*- coding utf-8 -*-
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  kontakt@markusritschel.de
# Date:   11/10/2020
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
from mpim_icelab.harps import salinity_harps
from .salinity_harps import read_salinity_harps
from .light_harps import read_light_harps
from .helpers import *


# calc_brine_salinity = salinity_harps.calc_brine_salinity
read_light_harp = read_light_harps
read_salinity_harp = read_salinity_harps
