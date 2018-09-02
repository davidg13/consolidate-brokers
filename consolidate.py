#!/usr/bin/python3
import sys
from brokers.brokers import consolidate_brokers_exact

COLS_TO_COMPARE = [3,5,10,12]

infile = sys.argv[1]
outfile = sys.argv[2]

consolidate_brokers_exact(infile, COLS_TO_COMPARE, outfile)

