#!/usr/bin/env python

import os
import subprocess
import json
import re

import cgtools

# get directory of this file @i @python
PLUGIN_HOME = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = PLUGIN_HOME + "/../data/locations.log"
WINDOW_TEXT = PLUGIN_HOME + "/../tmp/windowtext.txt"

class TagFile:

    def __init__(self, srcFileName):
        '''create tags for the file'''
        
        self.srcFileName = srcFileName
        self.tags = []

        [self.tags.append(Tag(ctagsLine = line)) for line in self.tagify_file(srcFileName)]

    def tagify_file(self, fileName):
        '''execute ctags on a specific file (with linenumber option and get the output'''

        # have to add the vimL mapping to prevent auto-sourcing from Pathogen
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

    def __repr__(self):
        return "\t".join([str(x) for x in (self.name, self.srcName, self.type)])

    def check_existence(self):
        with open(self.srcName, 'r') as f: 
            reg = self.truncate_regex()

            # why do I not have to escape these in vim? @wtodo @frequent-function @python 
            reg = reg.replace("(", "\(")
            reg = reg.replace(")", "\)")
            pat = re.compile(reg, re.MULTILINE)
            # existence of a regex in string @example @regex @python 
            if pat.search(f.read()): 
                return True
            else:
                return False

    def truncate_regex(self):

        tRegex = self.regex
        if self.regex[0] == "/":
            tRegex = self.regex[1:] 

        tRegex = tRegex.replace(r'/;"', "")
        return tRegex

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

def log_tag_info(srcFile, lineNum, colNum, fileExtension, logFile):
    
    #get the nearest tag, will return None if no tag match
    cBufferFN = PLUGIN_HOME + "/../tmp/cBuffers/cBuffer." + fileExtension
    
    nTag = get_nearby_tag(cBufferFN, lineNum, colNum)
  
    if nTag:
        #change the file name to not point to the temp file
        nTag.srcName = srcFile
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

def update_log(logFN):
    '''remove non-existing tags (file changed/deleted or refactored)
    and remove duplicate functions'''
    
    # re-factor log to class @wtodo @frequent-function
    tags = get_unique_tags(load_tags_from_log(logFN))

    # does the file even exist anymore?
    tags = [tag for tag in tags if os.path.exists(tag.srcName)]

    # debug level @programming @wtodo

    # does the function exist anymore, has it been refactored?
    tags = [tag for tag in tags if tag.check_existence()] 

    with open(logFN, 'w') as f:
        [f.write(tag.to_json() + "\n") for tag in tags]

def get_unique_tags(tags):
    '''tags are returned in order given
    [a,b,c] -> [a,b] (if c was not unique)'''

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

    # popping and appending reversed the list order
    uniqueTags.reverse()

    return uniqueTags

def load_tags_from_log(logFN):

    tags = []
    with open(logFN, 'r') as f:
        for jLine in f: 
            tags.append(Tag(jsonLine = jLine))

    return tags

def generate_mru_browser_text():

    #remove dups and non-existing first
    update_log(LOG_FILE)

    #get resulting tags and display in reverse order (log has newest at end)
    logTags = load_tags_from_log(LOG_FILE)
    logTags.reverse()
    
    with open(WINDOW_TEXT, 'w') as f:
        for tag in logTags:
            if tag.prototype:
                tName = tag.name + "(" + tag.prototype.replace("class:", "") + ")"
            else:
                tName = tag.name

            outText = tName + "\t" + os.path.basename(tag.srcName) + "\t" + str(tag.cursorOffsetLine) + "\t" + str(tag.cursorColumnNumber) + "\t" + tag.regex.replace(r'/;"', "") + "\t" + tag.srcName
            f.write(outText + "\n")

if __name__ == "__main__":
    import sys

    event = sys.argv[1]
    if event == "log":
        log_tag_info(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], LOG_FILE)
    elif event == "browsertext":
        generate_mru_browser_text()
    else:
        raise KeyError("Must Specify Event")
     
