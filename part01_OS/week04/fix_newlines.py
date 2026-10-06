#!/usr/bin/env python3 # this shebang makes the script run with python3
"""
fix_newlines.py
Reads a CSV file, removes embedded newlines from all fields,
and writes the result as a tab-separated (TSV) file.

Usage: python3 fix_newlines.py input.csv output.tsv
"""

import csv # imports a tool for reading and writing CSV files
import sys # imports system tools

# defines a function with input and output file paths as its arguments
def fix_newlines(input_path, output_path):
    rows_fixed = 0 # no fixed rows

# this opens the input file then the output file
    with open(input_path, newline='', encoding='utf-8') as infile, \
         open(output_path, 'w', newline='', encoding='utf-8') as outfile:

# reads and writes CSV rows one at a time
        reader = csv.reader(infile)
        writer = csv.writer(outfile, delimiter='\t')

# loops through each row and stores the number of the row and its contents
        for i, row in enumerate(reader):
            cleaned = []
            row_had_newline = False

# loops through every field in the current row and checks for newline characters
# then replaces them with spaces. If no newline is found in that row, the row will remain unchanged
            for field in row:
                if '\n' in field or '\r' in field:
                    cleaned.append(field.replace('\n', ' ').replace('\r', '').strip())
                    row_had_newline = True
                else:
                    cleaned.append(field)
# if any field in the row changes, one will be added to the number of corrected rows
            if row_had_newline:
                rows_fixed += 1
                print(f"  Row {i}: embedded newline removed", file=sys.stderr)

            writer.writerow(cleaned) # writes the clean version to the output file (tsv)

    print(f"Done. {rows_fixed} row(s) fixed.") #prints how many rows were fixed
    print(f"Output written to: {output_path}") # prints path to the output

if __name__ == '__main__':
    if len(sys.argv) != 3: # checks for the script name and 2 required file arguments
        print("Usage: python3 fix_newlines.py input.csv output.tsv") # shows usage when the # of arguments is wrong
        sys.exit(1) # stops the script due to the error

# this calls the function (input and output paths are used)
    fix_newlines(sys.argv[1], sys.argv[2])
