import re
import logging

from mruutility import first_non_whitespace_index, is_comment_line, is_blank_line

def test_near_tag():
    with open("./tests/mockFile1.py", 'r') as f:
        fileText = f.read()

    nearestFunc = py_get_nearest_tag(fileText, 1, 0)
    assert nearestFunc == None
    
    nearestFunc = py_get_nearest_tag(fileText, 3, 5)
    assert nearestFunc[1] == "def func_outside():"

    nearestFunc = py_get_nearest_tag(fileText, 5, 8)
    assert nearestFunc[1] == "def func_outside():"

    nearestFunc = py_get_nearest_tag(fileText, 10, 10)
    assert nearestFunc[1] == "def func_inside():"
     
    nearestFunc = py_get_nearest_tag(fileText, 16, 8)
    assert nearestFunc[1] == "def func_outside():"
    
    nearestFunc = py_get_nearest_tag(fileText, 17, 0)
    assert nearestFunc == None
    
def py_get_nearest_tag(fileText, lineNum, byteNum):
    '''
    cursor is in tag's scope.  Which tag?
    lineNum input is 1-based
    byteNum input is 0-based
    '''

    #get lines but preserve newlines
    fileLines = fileText.split("\n") 
    fileLines = ["%s\n" % x for x in fileLines]

    fxnDefPattern = re.compile(r'^(\s*)(def\s+\S+)\(', re.MULTILINE)

    currLine = lineNum - 1 
    currByte = byteNum
    while True:
        
        #get left most non-whitespace character
        #don't change the currByte if only whitespace or comments
        lineText = fileLines[currLine]
        logging.debug("l %s b %s", currLine, currByte)
        logging.debug("currentPosition [%s]", lineText[currByte:])
        
        #  maybe update tag object to know it's column definition position
        #move to the next line
        logging.debug( "checking for function")
        m = fxnDefPattern.match(lineText)
        if m:
            if m.start(2) < currByte: 
                logging.debug( m.group(2))
                return (currLine + 1, m.group(2))

        #check if non-coding line (blank or comment-only line)
        logging.debug("checking non-coding")
        if is_comment_line(lineText) or is_blank_line(lineText):
            logging.debug("  encountered non-coding line")
            if currLine == 0:
                return None
            currLine -= 1
            continue
        logging.debug(" not non-coding")

        #move to first coding character on line
        #  only if fnwi is less indented than the current position
        fnwi = first_non_whitespace_index(lineText)
        currByte = fnwi if (fnwi < currByte) else currByte
        if currByte == None:
            raise ValueError("Can't find coding byte on line")
        
        logging.debug(" fnwi [%s]",  lineText[currByte:])
        
        if currLine == 0:
            return None

        currLine -= 1 

if __name__ == "__main__":
    import sys
    assert sys.argv[1] in globals(), "Need name of fxn to run from command line!"
    fxnToRun = globals()[sys.argv[1]] 
    fxnToRun(*sys.argv[2:])
