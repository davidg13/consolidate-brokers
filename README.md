# Broker Consolidation Test

## Installation
- Create a python 3 virtual environment
- From the project root, run 
```
$pip install -r requirements.txt
```

## Running 
```
$python consolidate.py input_file output_file  
```
## Testing
From the project root, run
```
$pytest
```
## TODOs
- I started to work on fuzzy matching.  Plan was to group based on similar hash vectors, then do an n-squared comparison of records using some threshold of levenshtien distance between values to indicate a match
- Build up a command line tool for this using argparse to expose some nicer command line options
- Enable either exact or inexact match through the cli
- add tests fro writing files and the fuzzy matching
- add some quick tools for aggregating columns

## Data

Data file came from:
http://askebsa.dol.gov/FOIA%20Files/2016/Latest/F_SCH_A_PART1_2016_Latest.zip