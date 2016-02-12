#!/usr/bin/python

import sys

from Options import Options
from JiraProcessor import JiraProcessor

def main(argv):
    opts = Options('agileProgress.ini', argv)
    
    processor = JiraProcessor(opts)
    processor.processCompleted()

if __name__ == "__main__":
    main(sys.argv[1:])
