# Week 04: Inspecting and validating fossil datasets

`hello_researcher.sh`: Prints your username, today's date and the line count of otb_fossils.tsv. Usage: ./hello_researcher.sh
`inspect.sh`: Prints the number of rows and columns in one TSV file. Usage: ./inspect.sh otb_fossils.tsv
`dataset_info.sh`: Prints the row and column counts and a numbered list of header fields. Usage: `./dataset_info.sh otb_fossils.tsv`
`validate_tsv.sh`: Checks that a TSV file exists, is not empty and has the expected number of columns in every row. Usage: `./validate_tsv.sh otb_fossils.tsv 30`
`batch_inspect.sh`: Prints a table of row and column counts for every TSV file in a folder. Usage: `./batch_inspect.sh .`
`check_catalog_numbers.sh`: Lists catalog numbers that do not start with the expected prefix and saves them to `bad_catalog_numbers.log`. Usage: `./check_catalog_numbers.sh eppe_fossils.tsv "EP "`
`formation_counts.sh`: Counts OTB specimens from six formations (Koobi Fora, Shungura, Nachukui, Nawata, Kanapoi, Usno). Usage: `./formation_counts.sh otb_fossils.tsv`
`dataset_report.sh`: Writes a PASS/FAIL summary report for every TSV file in a folder and lists files with fewer than 100 rows in `small_files.log`. Usage: `./dataset_report.sh .`
`fix_newlines.py`: Converts a CSV file to TSV and removes line breaks inside fields. Usage: `python3 fix_newlines.py eppe_fossils.csv eppe_fossils.tsv`

