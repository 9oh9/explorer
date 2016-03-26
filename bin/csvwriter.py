#!/usr/bin/env python

import argparse
from app.utils import write_csv

parser = argparse.ArgumentParser()
parser.add_argument('in_file')
parser.add_argument('out_file')
args = parser.parse_args()

write_csv(args.in_file, args.out_file)
