import subprocess
import json
import os
import re

from mruutility import first_non_whitespace_index

PLUGIN_HOME = os.path.dirname(os.path.abspath(__file__))

class TagFile:

    def __init__(self, srcFileName):
        '''create tags for specific file'''
        
        self.srcFileName = srcFileName
        self.tags = []
        self.get_tags_in_file()

    def get_tags_in_file(self):

        [self.tags.append(Tag(ctagsLine = line)) for line in tagify_file(self.srcFileName)]

def tagify_file(fileName):
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
        self.lineNumber = None #1-based
        self.prototype = None
        self.ctagsLine = ctagsLine
        self.jsonLine = jsonLine
        self.fnwi = None

        #cursor location information (should re-factor)
        self.cursorOffsetLine = None
        self.cursorColumnNumber = None

        # optional initialization
        if ctagsLine:
            self.parse_ctags_output_line()
        elif jsonLine:
            self.from_json()
       
        # first character is always "^"
        self.fnwi = first_non_whitespace_index(self.regex[2:])

    def __repr__(self):
        return "\t".join([str(x) for x in (self.name, self.srcName, self.type)])

    def function_choice_output(self):
        
        if self.prototype:
            tName = self.name + "(" + self.prototype.replace("class:", "") + ")"
        else:
            tName = self.name

        whitespace = ' ' * 1000
        outText = tName + whitespace + '\t' + os.path.basename(self.srcName) + "\t" + str(self.cursorOffsetLine) + "\t" + str(self.cursorColumnNumber) + "\t" + self.regex.replace(r'/;"', "") + "\t" + self.srcName
        return outText

    def check_existence(self, cBufferFN):
        '''check if tag exists in file'''
      
        checkFN = self.srcName
        if cBufferFN == self.srcName:
            # search through the modified buffer instead
            checkFN = PLUGIN_HOME + "/../tmp/cBuffers/cBuffer." + self.srcName.split(".")[-1]

        with open(checkFN, 'r') as f: 
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
    print tFile
    for tag in tFile.tags:
        print tag.name
        print tag.lineNumber
        print tag.regex[2:]
        print tag.fnwi

if __name__ == "__main__":
    import sys
    assert sys.argv[1] in globals(), "Need name of fxn to run from command line!"
    fxnToRun = globals()[sys.argv[1]] 
    fxnToRun(*sys.argv[2:])

