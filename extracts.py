
from typing import List, Callable
from classes import *

X_HEADER_PREFIX = "x axis:"
Y_HEADER_PREFIX = "y axis:"

def extract_headers(lines :List[str], X_HEADER_PREFIX :str = X_HEADER_PREFIX, Y_HEADER_PREFIX :str = Y_HEADER_PREFIX):
    """
    finde the headers in the lines of the text for the X axis and Y axis
    """
    headerX = ''
    headerY = ''
    
    for line in lines:
        line_lower_case = line.lower()
        
        if line_lower_case.startswith(X_HEADER_PREFIX):
            
            headerX = line[len(X_HEADER_PREFIX):].strip()
        
        elif line_lower_case.startswith(Y_HEADER_PREFIX):
            
            headerY = line[len(X_HEADER_PREFIX):].strip()
            
        # if both of the header fond there is no reson to contine the loop
        if headerX and headerY:
            return headerX, headerY
        
    return headerX, headerY


def identify_rows_or_colloms (first_line :str):
    """
    identify is the given data is in rows, returns 'row', or colloms, returns 'collom'.
    """
    if first_line.replace(' ','') == '':
        return None
    
    # the number of word
    sum_words = 0
    
    for i in first_line:
        if i.isalpha():
            sum_words += 1

    if sum_words >= 2:
        return "collom"
    else :
        return "row"


A_HEADER_PREFIX = "a "
B_HEADER_PREFIX = "b "

def extract_parms_to_fit(lines :List[str], A_HEADER_PREFIX :str= A_HEADER_PREFIX, B_HEADER_PREFIX :str= B_HEADER_PREFIX):
    """
    get the values list for the paramater a and b frome the lines of the content of the file
    """
    paramA = {}
    paramB = {}
    for line in lines:
        if paramA and paramB:
            return paramA, paramB
        
        if line.startswith(A_HEADER_PREFIX) and not paramA :
            vars = line.split()
            paramA = {'start': float(vars[1]), 'end': float(vars[2]), 'step': float(vars[3])}
        
        if line.startswith(B_HEADER_PREFIX) and not paramB :
            vars = line.split()
            paramB = {'start': float(vars[1]), 'end': float(vars[2]), 'step': float(vars[3])}
    
    return paramA, paramB

