import os

PLUGIN_HOME = os.path.dirname(os.path.abspath(__file__))
DLOG_FILE = PLUGIN_HOME + "/../debug.txt"

def dlog(outString):
    with open(DLOG_FILE, 'a') as f:
        f.write(str(outString) + "\n")
