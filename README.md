# MPIM Ice-Lab Routines

![build](https://github.com/markusritschel/mpim-icelab/workflows/build/badge.svg)
[![License MIT license](https://img.shields.io/github/license/markusritschel/mpim-icelab)](./LICENSE)


A collection of routines for various tasks related to the sea-ice laboratory of the Max-Planck-Institute for Meteorology in Hamburg


## Installation
Via pip:
```bash
pip install git+https://github.com/markusritschel/mpim-icelab.git
```

Or, for installing from the sources (with the option to update via a simple `git pull`): <br>
Clone this repo via
```bash
git clone https://github.com/markusritschel/mpim-icelab
```
Then, in the new directory (`cd mpim-icelab/`) install the package via:
```
python setup.py install
```
or via one of the following
```
python setup.py develop
pip install -e .
```
if you plan on making changes on the code.


## Usage
For some examples of usage, have a look at the Jupyter notebooks in `./notebooks/`.
They explain some of the package's functionalities.


## Testing
To test the code, run `make test` in the source directory.
This will execute both the unit tests and docstring examples (using pytest).

Run `make coverage` to generate a test coverage report and `make lint` to check code style consistency.


## TODO
* [ ] Add examples in Jupyter Notebook for TSTICKS


## Maintainer
- [markusritschel](https://github.com/markusritschel)


## Contact & Issues
For any questions or issues, please contact me via git@markusritschel.de or open an [issue](https://github.com/markusritschel/mpim-icelab/issues).


---
&copy; Markus Ritschel 2020
