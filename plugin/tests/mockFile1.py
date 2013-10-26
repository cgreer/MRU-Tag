import os

def func_outside():    
    ''' blah blah doc blah blah'''

    if "hello" == "world":
        return None

    def func_inside():
        
        while True:
            print "hello"

    #test outside
    if "hello":
        print "nothing"

