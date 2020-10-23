# !/usr/bin/env python
# -*- coding utf-8 -*-
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  kontakt@markusritschel.de
# Date:   11/10/2020
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import pandas as pd
import xarray as xr

from mpim_icelab.harps.helpers import median, grad, savgol


logger = logging.getLogger(__name__)


def read_harp(file, debug=False, **kwargs):
    """Read-out routine for log files of the salinity harps developed by Leif Riemenschneider.
    Non-valid characters get eliminated such that only numeric values remain.
    A xarray.Dataset is created with `time`, `module` and `wire_pair` as coordinates.

    Return
    ------
    ds : xarray.Dataset
        Converted DataFrame to xarray Dataset. Similar to netCDF structure.
    """

    # specify column names for entries of the data file
    col_names = ['device', 'time', 'r2', 'd2', 'r16', 'd16', 'temperature', 'logger_temp']

    logger.info('read salinity harp now...')

    # read csv file into Pandas DataFrame
    df = pd.read_csv(file, names=col_names, index_col=False,
                     skiprows=0, comment='#', sep=' ',
                     engine='python', error_bad_lines=False)

    # split first column into harp-module number and wire-pair number and remove the origin column
    df = df.join(df['device'].str.split(':', 2, expand=True).iloc[:, :2].rename(columns={0: 'module', 1: 'wire_pair'}))

    # remove redundant columns
    df.drop(['device'], inplace=True, axis=1, errors='ignore')

    # convert content of 'time' column to datetime objects
    df['time'] = pd.to_datetime(df['time'], errors='coerce')  # 'coerce' errors yields NA for non datetime strings
    # drop rows with non datetime objects and set time as index
    df = df.dropna(subset=['time'])
    df.set_index(['time'], inplace=True)

    # make remaining columns numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    # make 'module' and 'wire_pair' column additional index
    df.set_index(['module', 'wire_pair'], append=True, inplace=True)

    df.sort_index(inplace=True)

    # convert multi index to multi column
    df = df.unstack(level=1).unstack(level=1)
    lastcol_idx = df.iloc[:, 0].dropna().index
    # ... and fill NANs in all columns backwards such that in each row with `lastcol_idx` are
    # all values of one block
    df.fillna(method='bfill', inplace=True)

    # now limit data frame to those respective rows
    df = df.loc[lastcol_idx]#[:-1]  # last row has only one single value in column 1

    # convert back to multi index
    df = df.stack(level=1).stack()
    ds = df.to_xarray()

    # ensure time coordinate is datetime object
    ds.coords['time'] = pd.to_datetime(ds.time.values)

    populate_attrs(ds)

    if not kwargs.pop('debug', None):
        ds = ds.drop(labels=['d2','d16','logger_temp'])

    return ds


def calc_brine_salinity(T, method='Assur', print_formula=False):
    """Calculate the brine salinity by a given temperature according to one of the following methods:
    - 'Assur'
        year: 1958
        S = -1.20 - 21.8*T - 0.919*T**2 - 0.0178*T**3

    - 'N&W09'
        author: Notz & Worster
        year: 2009
        S = -21.4*T - 0.886*T**2 - 0.0170*T**3

    - 'Vancoppenolle'
        year: 2019
        doi: 10.1029/2018JC014611
        S = -18.7*T - 0.519*T**2 - 0.00535*T**3

    Parameters
    ----------
    T : float
        Temperature in °C
    """
    # TODO: add validity range and mask T/S accordingly
    # import numpy as np
    # T_check = np.all(T < 30) & np.all(T > -70)
    # assert T_check, "Argument 'T' out of range"

    if method == 'Assur':
        a = c = d = 0
        b = -18.4809
    elif method == 'N&W09':
        a = 0
        b = -21.4
        c = -0.886
        d = -0.0170
    elif method == 'Vancoppenolle':
        a = 0
        b = -18.7
        c = -0.519
        d = -0.00535
    else:
        raise KeyError("Method unknown!")

    logger.info('Using %s method for calculating the brine salinity', method)

    S_brine = a + b*T + c*T**2 + d*T**3

    if print_formula:
        print('-'*60)
        print(f'For {method}, the S_brine gets calculated according to')
        print('\tS_brine = a + b*T +c*T**2 +d*T**3')
        print('with: ')
        print(f'\ta = {a}')
        print(f'\tb = {b}')
        print(f'\tc = {c}')
        print(f'\td = {d}')
        print()

    return S_brine


def calc_freezing_starts(data, resistance_channel='r16', kind='median', tolerance=1e-4):
    resistance = data[resistance_channel]

    # smoothen the signal
    resistance_smooth = eval(kind)(resistance)
    # compute gradient of that smoothened signal
    resistance_grad = eval(kind)(grad(resistance_smooth, 20))

    # set all values below a certain threshold to nan and remove them
    condition = resistance_grad > tolerance
    grad_gt_tol = resistance_grad.where(~condition, 9999)
    # alternative:
    # grad_tol = resistance_grad.where(condition, drop=True)

    # then, find the index of the first occurrence
    freezing_starts = grad_gt_tol.argmax('time')
    # alternative:
    # freezing_starts = grad_tol.argmin('time')

    return data.time[freezing_starts].where(freezing_starts > 0)


@xr.register_dataset_accessor("seaice")
class SalinityHarpsAccessor:
    def __init__(self, xarray_obj):
        self._obj = xarray_obj

    def calc_ice_properties(self, **kwargs):
        ds = self._obj
        r_ch = kwargs.pop('resistance_channel', 'r16')
        r_tol = kwargs.pop('r_tol', 1e-4)
        brine_sal_method = kwargs.pop('brine_sal_method', 'Vancoppenolle')

        freezing_starts = calc_freezing_starts(self._obj, resistance_channel=r_ch, tolerance=r_tol)
        resistance = ds[r_ch]
        T_freeze = ds['temperature'].sel(time=freezing_starts)

        T_input = ds['temperature'].where(ds['temperature'] < T_freeze)
        S_brine = calc_brine_salinity(T_input, method=brine_sal_method)

        r0s = resistance.sel(time=freezing_starts)
        liquid_frac = r0s / ds[r_ch]
        liquid_frac = liquid_frac.where(liquid_frac <= 1)
        solid_frac = 1 - liquid_frac
        S_bulk = liquid_frac * S_brine

        ds = ds.assign({'brine_salinity': S_brine,
                        'bulk_salinity': S_bulk,
                        'solid_fraction': solid_frac,
                        'liquid_fraction': liquid_frac,
                        # 'temperature_freeze': T_freeze
                       })

        populate_attrs(ds)

        return ds


def populate_attrs(ds):
    _attrs_dict = dict(
        temperature={'long_name': 'Temperature',
                     'units': '°C',
                     'comment': 'Temperature inside the ice body',
                     'description': 'Temperature at a certain level (associated with the respective wire pair) inside the ice body'
                     },
        brine_salinity={'long_name': 'Salinity of brine',
                        'units': 'g/kg',
                        'comment': 'Salinity of brine',
                        'description': 'Salinity of brine'
                        },
        bulk_salinity={'long_name': 'Bulk Salinity',
                       'units': 'g/kg',
                       'comment': 'Bulk Salinity',
                       'description': 'Bulk Salinity'
                       },
        solid_fraction={'long_name': 'Solid fraction',
                        'units': '',
                        'comment': 'Solid fraction',
                        'description': 'Solid fraction'
                        },
        liquid_fraction={'long_name': 'Liquid fraction',
                         'units': '',
                         'comment': 'Liquid fraction',
                         'description': 'Liquid fraction'
                         },
        logger_temp={'long_name': 'Temperature',
                     'units': '°C',
                     'comment': 'Temperature inside the ice body',
                     'description': 'Temperature at a certain level (associated with the respective wire pair) inside the ice body'
                     },
        r16={'long_name': 'Resistance r16',
             'units': 'Ω',
             'comment': 'Resistance at 16 Hz',
             'description': 'Resistance at 16 Hz'
             },
        r2={'long_name': 'Resistance r2',
            'units': 'Ω',
            'comment': 'Resistance at 2 Hz',
            'description': 'Resistamce at 2 Hz'
            },
        d16={'long_name': 'Debug flag for r16',
             'units': '',
             'comment': 'Debug flag for r16',
             'description': 'Debug flag for r16'
             },
        d2={'long_name': 'Debug flag for r2',
            'units': '',
            'comment': 'Debug flag for r2',
            'description': 'Debug flag for r2'
            },
        wire_pair={'long_name': 'Wire pair'},
        time={'long_name': 'Time'},
        )

    for var, sd in _attrs_dict.items():
        if var in ds.variables:
            for k, v in sd.items():
                ds[var].attrs[k] = v
    return ds
