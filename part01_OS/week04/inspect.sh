#!/usr/bin/env bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <dataset.tsv>"
    exit 1
fi

DATA="$1"
DATE=$(date)

# Check that the file exists
if [ ! -f "$DATA" ]; then
    echo "Error: file does not exist: $DATA"
    exit 1
fi

echo "Dataset: $DATA"
echo "Date: $DATE"
echo "I am: $(whoami)"
echo "Number of rows: $(($(wc -l < "$DATA") - 1))"
echo "Number of columns: $(awk -F '\t' 'NR == 1 {print NF}' "$DATA")"
