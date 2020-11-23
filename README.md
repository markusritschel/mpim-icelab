# MPIM Ice-Lab Routines

![build](https://github.com/markusritschel/mpim-icelab/workflows/build/badge.svg)
[![License MIT license](https://img.shields.io/github/license/markusritschel/mpim-icelab)](./LICENSE)


A collection of routines for various tasks related to the sea-ice laboratory of the Max-Planck-Institute for Meteorology in Hamburg


## Installation
The simplest way to install the package is via pip:
```bash
pip install git+https://github.com/markusritschel/mpim-icelab.git
```
For any future updates simply rerun the command again.

However, one can also install from the sources (with the option to update via a simple `git pull`): <br>
Therefore, clone this repo via
```bash
git clone https://github.com/markusritschel/mpim-icelab
```
Then, in the new directory (`cd mpim-icelab/`) install the package via:
```
python setup.py install
```
If you intend to perform changes on the source code, then an installation by using one of the following commands is suggested:
```
python setup.py develop
pip install -e .
```
This reflects any changes in the source code directly in the installed instance without the need of updating the installation.


## Usage
For some examples of usage, have a look at the Jupyter notebooks in the [notebooks](notebooks) directory.
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
