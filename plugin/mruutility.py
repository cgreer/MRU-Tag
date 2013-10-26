import re

def first_non_whitespace_index(lineText):
    '''find the index of the first non-whitespace character on line'''
    pat = re.compile(r'(\s*)(\S)')
    m = pat.match(lineText)
    if m:
        # start(2) gets start of 2nd group
        return m.start(2)
    else:
        return None

def is_comment_line(lineText):
    pat = re.compile(r'\s*(#|\'\'\'|\"\"\")')
    return bool(pat.match(lineText))

def is_blank_line(lineText):
    pat = re.compile(r'\s*\n')
    m = pat.match(lineText)
    return bool(m)

