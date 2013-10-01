#!/usr/bin/env python

import os

# get directory of this file @i @python
PLUGIN_HOME = os.path.dirname(os.path.abspath(__file__))

class FxnLocation:

    def __init__(self, name, fileName, lineNumber, columnNumber):
        self.name = name
        self.fileName = fileName
        self.lineNumber = lineNumber
        self.columnNumber = columnNumber

class FxnLocationCollection:

    def __init__(self):
        self.fxns = []

    def output_mru_list(self):
        ''' retain only unique and "newest" location
        e.g., if same function has been used but different columnNumber -> just keep mru 
        '''
        
        # collapse to unique fxn locations only 
        relevantLocations = []
        addedFxns = set()
        for fxnLocation in reversed(self.fxns):
            fxnIdentifier = fxnLocation.fileName + fxnLocation.name
            if fxnIdentifier not in addedFxns:
                relevantLocations.append(fxnLocation)
                addedFxns.add(fxnIdentifier)

        # print output
        with open(PLUGIN_HOME + "/.mrufxns", 'w') as f:
            for fxnLocation in relevantLocations:
                f.write("\t".join([fxnLocation.name, fxnLocation.fileName,
                    str(fxnLocation.lineNumber),
                    str(fxnLocation.columnNumber)]) + "\n")
        

def get_mru_fxn_list(mrufxndata):

    # rename data file "log" @wtodo @frequent-function

    # splitcasted data @wtodo @programming @python
    '''
    e.g.
    for name, fileName, lineNumber in cgtools.splitcaster(mrufxndata, ['str', 'str', 'int']):
      fxnLog.append(FxnLocation(name, fileName, lineNumber))

    '''

    #get log of mru fxns
    fxnLog = FxnLocationCollection()
    with open(mrufxndata, 'r') as f:
        for line in f:
            name, fileName, lineNumber, columnNumber = line.strip().split("\t")
            lineNumber, columnNumber = int(lineNumber), int(columnNumber)
            fxnLog.fxns.append(FxnLocation(name, fileName, lineNumber, columnNumber))

    fxnLog.output_mru_list()

if __name__ == "__main__":

    get_mru_fxn_list(PLUGIN_HOME + "/.mrufxndata")
 
