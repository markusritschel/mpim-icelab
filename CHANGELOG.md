# Change Log

All notable changes to this project will be documented in this file.

## 0.1.0

- Added routines for dealing with files from the salinity harp, the CTDs and the Tsticks.
- `read_ctd` works with either an output file from the RBR or SeaTerm software or with a log file retrieved from the MicroCat Seabird CTD via minicom.
- For the salinity harps there exists a xarray accessor `seaice` providing the method `calc_ice_properties`, which computes the quantities brine salinity, bulk salinity, solid fraction and liquid fraction based on the values measured by the salinity harp (i.e. temperature and resistance).
