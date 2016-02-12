#!/usr/bin/python

import sys
import os

from Options import Options
from JiraProcessor import JiraProcessor

def main(argv):
    opts = Options('epicProgress.ini', argv)
    
    processor = JiraProcessor(opts)
    
    os.remove(opts.outputFile) if os.path.exists(opts.outputFile) else None
    
    epics = opts.epics.split(",")
    for epic in epics:
        print("processing epic " + epic)
        processor.processEpic(epic)

if __name__ == "__main__":
    main(sys.argv[1:])
