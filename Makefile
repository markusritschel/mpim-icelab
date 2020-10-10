export SHELL := /bin/bash

test:
	pytest -n auto --doctest-modules mpim_icelab

coverage:
	pytest -n auto --doctest-modules --cov=seaborn --cov-config=.coveragerc mpim_icelab

lint:
	flake8 mpim_icelab
