#!/usr/bin/env python

import os
import subprocess
import json

import cgtools

# get directory of this file @i @python
PLUGIN_HOME = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = PLUGIN_HOME + "/locations.log"
WINDOW_TEXT = PLUGIN_HOME + "/windowtext.txt"

class TagFile:

    def __init__(self, srcFileName):
        '''create tags for the file'''
        self.srcFileName = srcFileName
        self.tags = []

        [self.tags.append(Tag(ctagsLine = line)) for line in self.tagify_file(srcFileName)]

    def tagify_file(self, fileName):
        '''execute ctags on a specific file (with linenumber option and get the output'''
        ctagProcess = subprocess.Popen(["ctags", "--fields=+n", "-f", "-", fileName], stdout=subprocess.PIPE) 
        fOutput = ctagProcess.stdout.readlines()

        return fOutput

class Tag:

    def __init__(self, ctagsLine = None, jsonLine = None):
        self.name = None
        self.srcName = None
        self.regex = None
        self.type = None
        self.lineNumber = None
        self.prototype = None
        self.ctagsLine = ctagsLine
        self.jsonLine = jsonLine

        #cursor location information (should re-factor)
        self.cursorOffsetLine = None
        self.cursorColumnNumber = None

        # optional initialization
        if ctagsLine:
            self.parse_ctags_output_line()
        elif jsonLine:
            self.from_json()

    def parse_ctags_output_line(self):

        ls = self.ctagsLine.strip().split("\t")
        self.name = ls[0]
        self.srcName = ls[1]
        self.regex = ls[2]
        self.type = ls[3]
        self.lineNumber = int(ls[4].replace("line:", ""))
        try:
            self.prototype = ls[5]
        except IndexError:
            self.prototype = None 

    def to_json(self):
        # make a json dict maker @wtodo @python 
        jDict = {"name": self.name,
                 "srcName": self.srcName,
                 "regex": self.regex,
                 "type": self.type,
                 "lineNumber": self.lineNumber,
                 "prototype": self.prototype,
                 "cursorOffsetLine": self.cursorOffsetLine,
                 "cursorColumnNumber": self.cursorColumnNumber
                 }

        return json.dumps(jDict)

    def from_json(self):
       objProperties = json.loads(self.jsonLine.strip()) 
       for attName, attProp in objProperties.items():
           setattr(self, attName, attProp)

def test_tagify(srcFileName):
    '''just testing if ctagging works'''
    tFile = TagFile(srcFileName)
    print tFile.tags[0].name

def log_tag_info(srcFile, lineNum, colNum, logFile):
    
    print "logging tag info"
    #get the nearest tag
    nTag = get_nearby_tag(srcFile, lineNum, colNum)
  
    if nTag:
        with open(logFile, 'a') as f:
            f.write(nTag.to_json() + "\n")
    else:
        print "no tags"

def get_nearby_tag(srcFile, lineNum, colNum, tagTypes = "fm"):
    ''' f = function, m = method '''
    lineNum, colNum = int(lineNum), int(colNum)
    tFile = TagFile(srcFile)
    lineNum_tag = cgtools.groupby(tFile.tags, "lineNumber")

    for i in xrange(lineNum, 0, -1):
        if i in lineNum_tag:
            nearTag = lineNum_tag[i][0]
            if nearTag.type in tagTypes:
                nearTag.cursorOffsetLine = lineNum - i
                nearTag.cursorColumnNumber = colNum
                return nearTag 

    # no tag was found
    return None

def generate_mru_browser_text():

    tags = []
    with open(LOG_FILE, 'r') as f:
        for jLine in f: 
            tags.append(Tag(jsonLine = jLine))

    uniqueProps = set()
    uniqueTags = []
    while True:    
        if not tags:
            break

        currTag = tags.pop()
        tagUniqueProps = (currTag.name, currTag.srcName, currTag.prototype)
        if tagUniqueProps not in uniqueProps:
            uniqueTags.append(currTag)
            uniqueProps.add(tagUniqueProps)

    #output
    with open(WINDOW_TEXT, 'w') as f:
        for tag in uniqueTags:
            if tag.prototype:
                tName = tag.name + "(" + tag.prototype.replace("class:", "") + ")"
            else:
                tName = tag.name

            outText = tName + "\t" + os.path.basename(tag.srcName) + "\t" + str(tag.cursorOffsetLine) + "\t" + str(tag.cursorColumnNumber) + "\t" + tag.regex.replace(r'/;"', "") + "\t" + tag.srcName
            f.write(outText + "\n")

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

    #get log of mru fxns
    fxnLog = FxnLocationCollection()
    with open(mrufxndata, 'r') as f:
        for line in f:
            name, fileName, lineNumber, columnNumber = line.strip().split("\t")
            lineNumber, columnNumber = int(lineNumber), int(columnNumber)
            fxnLog.fxns.append(FxnLocation(name, fileName, lineNumber, columnNumber))

    fxnLog.output_mru_list()

if __name__ == "__main__":
    import sys

    event = sys.argv[1]
    if event == "log":
        log_tag_info(sys.argv[2], sys.argv[3], sys.argv[4], LOG_FILE)
    elif event == "browsertext":
        generate_mru_browser_text()
    else:
        raise KeyError("Must Specify Event")
     
