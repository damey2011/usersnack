#!/bin/sh

set -ex

black . --check
mypy .
flake8
isort --check .
