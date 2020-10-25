# !/usr/bin/env python
# -*- coding utf-8 -*-
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  kontakt@markusritschel.de
# Date:   25/10/2020
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import pandas as pd
import xarray as xr


logger = logging.getLogger(__name__)


def read_light_harp(file):
    """Reads a log file of a light harp designed by Leif Riemenschneider. The log file is in tabular form of the format
        idx s:d:a: time C R G B logger_temperature

        idx : integer index keeping track of continuous measurements
        s   : stick
        d   : diode
        a   : amplifier
        C   : clear channel
        R   : red channel
        G   : green channel
        B   : blue channel

    Data get converted into and returned as an xarray.Dataset.
    """
    col_names = ['cnt', 'identifier', 'time', 'C', 'R', 'G', 'B', 'logger_temp']
    df = pd.read_csv(file, names=col_names, index_col=0, sep=r"\s+", comment='#',
                     engine='python', error_bad_lines=False)

    if not df.index.is_unique:
        raise ValueError("Index is not unique. Please check file and clean it if necessary.")

    df_sda = df['identifier'].str.strip(':')\
                             .str.split(':', 2, expand=True)\
                             .rename(columns={0: 'stick', 1: 'diode', 2: 'amplifier'})

    df = df_sda.join(df.drop(['identifier'], axis=1))

    df['time'] = pd.to_datetime(df['time'], errors='coerce')  # 'coerce' errors yields NA for non datetime strings
    df['time'] = df.time.dt.tz_localize(None)  # remove timezone info
    df = df.dropna(subset=['time'])
    df.set_index(['time'], inplace=True)

    df = df.apply(pd.to_numeric, errors='coerce')

    df.set_index(['stick', 'diode', 'amplifier'], append=True, inplace=True)

    # store column order
    _cols = df.columns

    df = df.unstack(level=[1, 2, 3])

    # lastcol_idx = df.iloc[:, 0].index
    firstcol_idx = df.dropna(subset=[('C', 0, 0, 0)]).index
    # ... and fill NANs in all columns backwards such that in each row with `lastcol_idx` are
    # all values of one block
    df.fillna(method='ffill', inplace=True)

    # now limit data frame to those respective rows
    df = df.loc[firstcol_idx][1:]  # first row has only one single value in column 1

    # convert back to multi index
    df = df.stack(level=[1, 2, 3])

    # restore original order of the columns
    df = df[_cols]

    ds = df.to_xarray()

    return ds
