# !/usr/bin/env python
# -*- coding utf-8 -*-
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  kontakt@markusritschel.de
# Date:   11/10/2020
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import io
import logging
import numpy as np
import pandas as pd
import re

import xmltodict


logger = logging.getLogger(__name__)


def read_ctd(file, **kwargs):
    """Check for file type and call respective reader function."""

    # select reader function based on first line of file
    with open(file, 'r') as f:
        line = f.readline().rstrip()
        # yields the first non-empty line
        while not line:
            line = f.readline().rstrip()

        # select reader function based on first line
        if line.startswith('* Sea-Bird'):
            ctd_reader_func = read_seabird
        elif line.startswith('RBR'):
            ctd_reader_func = read_rbr
        elif re.match(r"^#\s+(-*\d+\.\d+,\s+)+", line):
            ctd_reader_func = read_seabird_serial_log
        else:
            raise IOError("Couldn't identify file type. Expect the file to start with either '* Sea-Bird', 'RBR', "
                          "or a Seabird stream format like '#   1.8445,  3.05390,    0.568,  34.8722, 28 Mar 2019, 18:00:01'")

    logger.debug('read CTD file %s with %s routine', file, ctd_reader_func)

    df = ctd_reader_func(file, **kwargs)

    return df


def read_seabird(file: str, **kwargs):
    """Read SeaBird CTD internal log file.
    Parameters
    ----------
    file : str
        Path to the log file which shall be parsed.
    nan_flag : float
        Float which marks a missing entry in the log file.
    kwargs['verbose'] : bool
        Optionally print out header information of the log file.

    Return
    ------
    ds : pandas.DataFrame
        A pandas.DataFrame object containing all the variables from the log file.
    """
    # parse header
    row_no = 0
    xml_header = ""
    with open(file, 'r') as f:
        var_dict = dict()
        var_names = []
        units = []
        start_time = None
        sample_interval = None
        while True:
            line = next(f, None)
            row_no += 1
            if line.startswith('*END*'):    # end of header
                break

            line = line.strip('*').strip()

            # read first part into xml structure
            rx = re.match(r'^(\s*<.+>\s*)$', line)
            if rx:
                xml_header += rx.group(0)
                logger.debug(f"Found xml header")

            # get names and units
            rx = re.match(r'^# name (?P<id>\d) = (?P<variable>.+?): (?P<name>.+?) \[(?P<unit>.+?)\].*$', line)
            if rx:
                var_dict[rx.group('name')] = {'unit': rx.group('unit'),
                                              'var_id': rx.group('variable'),
                                              'id'  : rx.group('id')}
                var_names.append(rx.group('name'))
                units.append(rx.group('unit'))
                logger.debug(f"Found variable {rx.group('variable')} (unit: rx.group('unit'), name: rx.group('name'))")

            # get logging interval
            # rx = re.match(r'^# interval = (?P<unit>\w+?): (?P<value>\d+)', line)
            rx = re.match(r'^sample interval = (?P<sample_interval>\d+ \w+)', line)
            if rx:
                # interval = pd.Timedelta('{} {}'.format(rx.group('value'), rx.group('unit')))
                sample_interval = pd.Timedelta(rx.group('sample_interval'))
                logger.debug(f"Found sample time: {sample_interval}")

            # get start time
            rx = re.match(r'^# start_time = (.+) \[.+\]', line)
            if rx:
                start_time = pd.to_datetime(rx.group(1))
                logger.debug(f"Found start time: {start_time}")

            # get bad_flag
            rx = re.match(r'^# bad_flag = ([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)', line)
            if rx:
                bad_flag = rx.group(1)
                logger.debug(f"Found bad_flag: {bad_flag}")

    if not var_names:
        raise IOError("No variable names found in header! Please check input file.")
    if not start_time:
        raise IOError("No start time found in header! Please check input file.")
    if not sample_interval:
        raise IOError("No logging interval value found in header! Please check input file.")

    # modify names such that there are no blank spaces in between elements
    var_names[:] = [re.sub(r"[,]*\s+", "_", var).lower() for var in var_names]
    # var_names = [entry.replace('_Practical', '') for entry in var_names]

    units_dict = {var.lower(): unit.split(',')[-1].strip() for (var, unit) in zip(var_names, units)
                  if not var.lower().startswith('time')}

    # read rest of the file into a pandas DataFrame
    df = pd.read_csv(file, skiprows=row_no, sep=r"\s+", names=var_names,
                     usecols=range(len(var_names)))

    # remove 'time' column
    df = df.drop([i for i in var_names if 'time' in i.lower()], axis=1, errors='ignore')

    # ensure all column dtypes are numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    # generate time series and set as index
    time_idx = pd.date_range(start=start_time, periods=len(df), freq=sample_interval)
    df.index = time_idx
    df.index = df.index.round(sample_interval)

    df.index.name = 'time'

    # df.rename(columns={'Salinity_Practical': 'Salinity'}, inplace=True)

    # remove duplicates
    # for var in df.columns:
    #     duplicates = [item for item in df.columns if item.startswith(var)]
    #     duplicates = [item for item in duplicates if len(item) > len(var)]
    #     df.drop(duplicates, axis=1, errors='ignore', inplace=True)

    # take only columns that match unique var_names
    df = df[[var for var in set(var_names) if var in df.columns]]

    df = df.reindex(sorted(map(str.lower, df.columns)), axis=1)

    # set nan_flag as NAN
    df[df == bad_flag] = np.nan

    if 'verbose' in kwargs:
        print('{:<11}:'.format('Start time'), start_time)
        print('{:<11}:'.format('End time  '), time_idx[-1])
        print('{:<11}:'.format('Interval'), sample_interval)
        print('Variables and units:')
        for var, unit in units_dict.items():
            print('\t{:<12} : {}'.format(var, unit))
        print()

    # logger.info(f'Start time      : {start_time}')
    # logger.info(f'End time        : {time_idx [-1]}')
    # logger.info(f'Sample Interval : {interval}')
    # for var, unit in units_dict.items():
    #     logger.info(f'\t{var:<12} : {unit}')

    ds = df.to_xarray()
    # ds.attrs = units_dict

    attrs_dict = dict(
        temperature={'long_name': 'Temperature',
                     'units': '°C',
                     'comment': 'Water temperature',
                     'description': 'Water temperature'
                     },
        potential_temperature={'long_name': 'Potential temperature',
                               'units': '°C',
                               'comment': 'Potential temperature',
                               'description': 'Potential temperature'
                               },
        conductivity={'long_name': 'Conductivity',
                      'units': 'S/m',
                      'comment': 'Conductivity',
                      'description': 'Conductivity'
                      },
        density={'long_name': 'Density',
                 'units': 'kg/m³',
                 'comment': 'Density',
                 'description': 'Density'
                 },
        pressure={'long_name': 'Pressure',
                  'units': 'psi',
                  'comment': 'Pressure',
                  'description': 'Pressure'
                  },
        salinity={'long_name': 'Salinity',
                            'units': 'psu',
                            'comment': 'Salinity',
                            'description': 'Salinity'
                            },
        salinity_practical={'long_name': 'Practical Salinity',
                            'units': 'psu',
                            'comment': 'Practical Salinity',
                            'description': 'Practical Salinity'
                            },
        time={'long_name': 'Time'},
        )
    populate_attrs(ds, attrs_dict)

    xml_header = "<root>" + xml_header + "</root>"
    xml_dict = xmltodict.parse(xml_header)

    return ds


def read_seabird_serial_log(file, **kwargs):
    """Return xarray.Dataset"""
    with open(file, 'r') as f:
        lines = filter(None, (line.rstrip() for line in f))  # omit empty lines
        lines = list((line.lstrip('#') for line in lines))

    col_names = ['temperature', 'conductivity', 'pressure', '_date', '_time']
    # Salinity is not included by default. Can be changed in SeaTerm (under Windows)
    if len(lines[0].split(',')) == 6:
        col_names.insert(3, 'salinity')

    units = {'Temperature':  '°C',
             'Conductivity': 'S/m',
             'Pressure':     'dbar',
             'Salinity':     'psu'}

    df = pd.read_csv(io.StringIO('\n'.join(lines)), names=col_names, parse_dates={'time': ['_date', '_time']})

    # create time and set as index
    # df['time'] = df.date.map(str) + df.time
    # df.drop(['date', 'time'], axis=1, inplace=True)
    # df['time'] = pd.to_datetime(df['time'])
    df.set_index(['time'], inplace=True)

    # ensure all column dtypes are numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    ds = df.to_xarray()

    attrs_dict = dict(
        temperature={'long_name': 'Temperature',
                     'units': '°C',
                     'comment': 'Water temperature',
                     'description': 'Water temperature'
                     },
        conductivity={'long_name': 'Conductivity',
                      'units': 'S/m',
                      'comment': 'Conductivity',
                      'description': 'Conductivity'
                      },
        pressure={'long_name': 'Pressure',
                  'units': 'psi',
                  'comment': 'Pressure',
                  'description': 'Pressure'
                  },
        salinity={'long_name': 'Salinity',
                  'units': 'psu',
                  'comment': 'Salinity',
                  'description': 'Salinity'
                  },
        time={'long_name': 'Time'},
        )
    populate_attrs(ds, attrs_dict)

    return ds


def read_rbr(file, nan_flag=-1000., **kwargs):
    """Read RBR CTD internal log file.
    Parameters
    ----------
    file : str
        Path to the log file which shall be parsed.
    nan_flag : float
        Float which marks a missing entry in the log file.
    kwargs['verbose'] : bool
        Optionally print out header information of the log file.

    Return
    ------
    ds : pandas.DataFrame
        A pandas.DataFrame object containing all the variables from the log file.
    """
    header = {'host_time'     : 'Host time',
              'log_time'      : 'Logger time',
              'log_start'     : 'Logging start',
              'log_end'       : 'Logging end',
              'sample_period' : 'Sample period'}

    with open(file, 'r') as f:
        # read header info and find number of lines to skip
        row_no = 0
        file_header = ""
        while True:
            line = next(f, None)
            row_no += 1
            # break on first empty line (= end of header)
            if line == '\n':
                break
            else:
                file_header += line  # + '\n'

        for k, v in header.items():
            m = re.search(r'^{}\s+(\d.+)$'.format(v), file_header, re.MULTILINE)
            if m:
                time_str = m.group(1)
                if len(time_str.split('/')) > 1:
                    header[k] = pd.to_datetime(time_str, format='%y/%m/%d %H:%M:%S')
                else:
                    header[k] = pd.Timedelta(time_str)

        # read in the rest if the file into a pandas DataFrame
        df = pd.read_csv(file, skiprows=row_no, sep=r"\s+")

    # ensure all columns are numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    # generate time series and set as index
    time_idx = pd.date_range(start=header['log_start'], end=header['log_end'], freq=header['sample_period'])
    df.index = time_idx[:len(df)]
    df.index = df.index.round(header['sample_period'])
    df.index.name = 'time'

    # set nan_flag as NAN
    df[df == nan_flag] = np.nan

    df.rename(columns={'Cond': 'Conductivity',
                       'Temp': 'Temperature',
                       'Pres': 'Pressure',
                       'Sal': 'Salinity',
                       'DensAnom': 'Density_anomaly'
                       }, inplace=True)

    df = df.reindex(map(str.lower, sorted(df.columns)), axis=1)

    if 'verbose' in kwargs:
        for k, v in header.items():
            print('{:<14}: {}'.format(k, v))
        print()

    ds = df.to_xarray()

    attrs_dict = dict(
        temperature={'long_name': 'Temperature',
                     'units': '°C',
                     'comment': 'Water temperature',
                     'description': 'Water temperature'
                     },
        potential_temperature={'long_name': 'Potential temperature',
                               'units': '°C',
                               'comment': 'Potential temperature',
                               'description': 'Potential temperature'
                               },
        conductivity={'long_name': 'Conductivity',
                      'units': 'mS/cm',
                      'comment': 'Conductivity',
                      'description': 'Conductivity'
                      },
        density_anomaly={'long_name': 'Density Anomaly',
                 'units': 'kg/m³',
                 'comment': 'Density Anomaly',
                 'description': 'Density Anomaly'
                 },
        pressure={'long_name': 'Pressure',
                  'units': 'psi',
                  'comment': 'Pressure',
                  'description': 'Pressure'
                  },
        salinity={'long_name': 'Salinity',
                  'units': 'psu',
                  'comment': 'Salinity',
                  'description': 'Salinity'
                  },
        time={'long_name': 'Time'},
        )
    populate_attrs(ds, attrs_dict)

    return ds


def populate_attrs(ds, attrs_dict):
    for var, sd in attrs_dict.items():
        if var in ds.variables:
            for k, v in sd.items():
                ds[var].attrs[k] = v
    return ds
