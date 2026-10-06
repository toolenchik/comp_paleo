## Project title: Computational Paleobiology
This repository contains the .sh scripts I wrote in Part 1 (operating systems) of ANT 388. 
The scripts inspect, validate and summarize tab-separated fossil specimen datasets. 
In class we used Omo-Turkana Basin (OTB) and EPPE collections, but the scripts can work on any tsv. It also records which software is installed on a Mac. The scripts check the arguments and prints a usage message.

## Course context 
ANT388, UT Austin, Fall'26

## Repository structure 
comp_paleo repo has a README, .gitignore, and folders for every course part. Each folder contains folders for each week's scripts. Every week has their own README, describing what the script does.

## Dependencies — what software is needed to run these scripts
MacOS 15.7.9
GNU bash, version 3.2.57(1)-release (arm64-apple-darwin24)
Python 3.14.7
Homebrew
Basic command line tools: wc, tr, head, tail,awk, grep, sed, etc.

## Usage — how to run the scripts, with at least two concrete examples
```
chmod +x *.sh
./*.sh or bash *.sh
```

Count OTB specimens by formation:
```
./formation_counts.sh otb_fossils.tsv
```

Convert a CSV to a clean TSV:
```
python3 fix_newlines.py eppe_fossils.csv eppe_fossils.tsv
```

## Data — where to obtain the datasets the scripts expect (PBDB API URL, Origins database URL)
otb_fossils.tsv`: Omo-Turkana Basin specimens Source: https://paleocore.org/origins/
eppe_fossils.csv: EPPE specimens Source: https://paleobiodb.org/data1.2/

## Author name and contact
Sai T
