import os
import json

class ExpandMenu(object):

    def __init__(self, menuLines = None):
        '''menuLines is an OrderedDict'''
        self.menuLines = menuLines
        self.expanded = []
        self.menuText = ""

        if self.menuLines:
            self.create_menu_text(self.menuLines)

    def create_menu_text(self, menuLines):
        '''1D Menu Only
        menuLines is an ORDERED DICT'''

        prefixSep = "  "
        self.menuText = " MRU-Tag (Files sorted by MRU.  Select file to see MRU tags)\n"
        whitespace = " " * 1000
        for i, fName in enumerate(menuLines):
            baseFileName = os.path.basename(fName)
            self.menuText += "+[" + str(i + 1) + "] " + baseFileName + "\n"
            self.menuText +=  prefixSep + "...go to " + baseFileName + whitespace + "\t" + fName + "\n"
            for i, tag in enumerate(menuLines[fName]):
                self.menuText += prefixSep + tag.function_choice_output() + "\n"

    def menu_lines(self):
        return self.menuText.split("\n")

    def output_menu(self, fName):

        tPrint = False
        eCounter = 0
        with open(fName, 'w') as f:
            for i, mLine in enumerate(self.menu_lines()):
                if is_expandable(mLine):
                    eCounter += 1
                    if eCounter in self.expanded:
                        f.write(mLine.replace("+[", "-[") + "\n")
                        tPrint = True
                    else:
                        f.write(mLine + "\n")
                        tPrint = False
                else:
                    # Title menu
                    if i == 0:
                        f.write(mLine + "\n")
                    # Everything else
                    elif tPrint: 
                        f.write(mLine + "\n")

    def handle_expansion_change(self, choice):

        # choice will be given as X of line in [X]
        choice = int(choice)
        if choice in self.expanded:
            self.expanded.remove(choice)
        else:
            self.expanded.append(choice)


    def load_from_file(self, fName):

        with open(fName, 'r') as f:
            self.from_json(f.readline())

    def save_to_file(self, fName): 

        with open(fName, 'w') as f:
            f.write(self.to_json())

    def to_json(self):
        # make a json dict maker @wtodo @python 
        jDict = {"menuText": self.menuText,
                 "expanded": self.expanded,
                 }

        return json.dumps(jDict)

    def from_json(self, jsonLine):
        objProperties = json.loads(jsonLine.strip()) 
        for attName, attProp in objProperties.items():
            setattr(self, attName, attProp)
    
def is_expandable(text):
    return text.startswith("+[") or text.startswith("-[")
