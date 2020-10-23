export SHELL := /bin/bash

test:
	pytest --doctest-modules tests/

coverage:
	pytest --doctest-modules --cov=seaborn --cov-config=.coveragerc mpim_icelab

lint:
	flake8 mpim_icelab
