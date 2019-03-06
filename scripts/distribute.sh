#!/bin/bash
# run this script to release this to pipy

(cd ./cli && (
    python3 setup.py sdist bdist_wheel &&
    twine upload dist/*
))