#!/bin/bash

# Run the Python script to generate the Markdown tables from CSV files
python convert_csv_to_md.py

# Build the Jupyter Book
jupyter-book clean .
jupyter-book build . 2>&1 | sed -E '/WARNING: duplicate (label|citation)/d'
rc=${PIPESTATUS[0]}
exit $rc