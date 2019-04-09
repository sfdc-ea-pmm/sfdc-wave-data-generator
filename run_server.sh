#!/bin/bash

cd docs/_build/html
python3 -m http.server $PORT
