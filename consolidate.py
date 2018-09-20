#!/usr/bin/env python
import argparse
from brokers.brokers import consolidate_brokers

parser = argparse.ArgumentParser(description='A consolidation program')
parser.add_argument('infile', help='File to read from')
parser.add_argument('outfile', help='File to write to')
parser.add_argument('cols', nargs='+', type=int, help='columns to compare') 
parser.add_argument('--exact', action='store_true')
args = parser.parse_args()


consolidate_brokers(args.infile, args.cols, args.outfile, exact=args.exact)


