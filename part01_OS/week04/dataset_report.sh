#!/usr/bin/env bash
# dataset_report.sh
# Generate a summary report of all TSV files in a directory.
# Usage: ./dataset_report.sh <directory>
#
# Author: Saida Tokmurzina
# Date: 09/18/2026

# ── Argument handling ────────────────────────────────────────────────────────
if [ $# -ne 1 ] || [ ! -d "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# ── Initialise counters and log file ─────────────────────────────────────────
DIRPATH="$1"
TOTAL_FILES=0
TOTAL_ROWS=0
SMALL_FILES=0
OVERALL="PASS"

# Clear the old log
> small_files.log

echo "Dataset Report"
echo "Directory: $DIRPATH"
echo "Generated: $(date '+%Y-%m-%d')"
echo "============================================================"


# ── Main loop: process each TSV file ─────────────────────────────────────────
for FILEPATH in "$DIRPATH"/*.tsv; do
    # Skip the loop if the directory has no TSV files
    [ -f "$FILEPATH" ] || continue

    FILENAME=$(basename "$FILEPATH")
    ROWS=$(awk 'END {if (NR > 0) print NR - 1; else print 0}' "$FILEPATH")
    COLS=$(awk -F'\t' 'NR == 1 {print NF}' "$FILEPATH")
    FIELDS=$(awk -F'\t' 'NR == 1 {print $1 " | " $2 " | " $3}' "$FILEPATH")
    BAD_ROWS=$(awk -F'\t' -v cols="$COLS" 'NF != cols {count++} END {print count+0}' "$FILEPATH")

    if [ "$BAD_ROWS" -eq 0 ]; then
        VALIDATION="PASS"
    else
        VALIDATION="FAIL"
        OVERALL="FAIL"
    fi

    echo ""
    echo "File: $FILENAME"
    echo "  Rows:    $ROWS"
    echo "  Columns: $COLS"
    echo "  Fields:  $FIELDS"
    echo "  Validation: $VALIDATION"

    if [ "$ROWS" -lt 100 ]; then
        echo "$FILENAME: $ROWS rows" >> small_files.log
        SMALL_FILES=$((SMALL_FILES + 1))
    fi

    TOTAL_FILES=$((TOTAL_FILES + 1))
    TOTAL_ROWS=$((TOTAL_ROWS + ROWS))
done


# ── Summary ───────────────────────────────────────────────────────────────────

echo ""
echo "============================================================"
echo "Summary"
echo "  Files processed: $TOTAL_FILES"
echo "  Total rows:      $TOTAL_ROWS"
echo "  Small files:     $SMALL_FILES"
echo "  Overall result:  $OVERALL"

if [ "$OVERALL" = "PASS" ]; then
    exit 0
else
    exit 1
fi


