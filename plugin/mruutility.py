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

def flatten(l, ltypes=(list, tuple)):
    '''Flatten multi-level lists of lists
    Credit: http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
   
    @flatten @python @list @example
    USAGE
    from cgtools import flatten

    a = [[1,2,3], [4,5,6]]
    allAs = flatten(a)
    '''

    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)

def groupby(listOfObjects, attributeName):
    '''
    group list of object by a property of the object 
    properties of each object must be of the same type 
    lists must not include complex types (no list of lists)
    '''

   
    allowableTypes = [type(x) for x in [1,'a', True, None, tuple(), list()]]

    attribute_objects = {} 
    for obj in listOfObjects:
        attributeValue = getattr(obj, attributeName) # @python @getattr @attribute @example   
        if type(attributeValue) not in allowableTypes:
            raise NameError("Attribute must be simple type or tuple") # custom error @wtodo @programming

        if type(attributeValue) == type(list()):
            attributeValue = tuple(sorted(attributeValue))

        attribute_objects.setdefault(attributeValue, []).append(obj)

    return attribute_objects

def groupbytraverse(listOfObjects, attributeName):
    '''
    group list of objects by the list elements of specified attributeName
    lists must be 1 dimensional
    
    Make an example @wtodo @cgtools @programming
    '''

    allowableTypesTraverse = [type(x) for x in [list(), tuple()]]
    allowableTypesSimple = [type(x) for x in [1,'a', True, None]]

    attribute_objects = {} 
    for obj in listOfObjects:
        attributeValue = getattr(obj, attributeName) 
        if type(attributeValue) not in allowableTypesTraverse:
            raise NameError("Attribute value type must be list or tuple")

        for element in attributeValue:
            if type(element) not in allowableTypesSimple:
                raise NameError("List element type must be simple")

            attribute_objects.setdefault(element, []).append(obj)

    return attribute_objects
