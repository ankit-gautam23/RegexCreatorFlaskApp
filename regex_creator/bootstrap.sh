#!/bin/sh
export FLASK_APP=./regex_code/index.py
pipenv run flask --debug run -h 0.0.0.0