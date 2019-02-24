#!/usr/bin/python3

from typing import List

labale_X  = 'x'
labale_Y  = 'y'
labale_dX = 'dx'
labale_dY = 'dy'


def pars_lines(lines_vars: List[List[str]]):
    """
    
    """

    index_x, index_dx, index_y, index_dy = revile_indexes(lines_vars)
    
    try:
        dataX  = [float(i) for i in lines_vars[index_x ][1::]]
        datadX = [float(i) for i in lines_vars[index_dx][1::]]
        dataY  = [float(i) for i in lines_vars[index_y ][1::]]
        datadY = [float(i) for i in lines_vars[index_dy][1::]]
    except ValueError as error:
        print("Input file error: Not all values can be convert to numbers")    
    
    return dataX, datadX, dataY, datadY
         
def revile_indexes(lines_vars: List[List[str]]):
    
    index_x, index_dx, index_y, index_dy = -1, -1, -1, -1

    for line_vas in enumerate(lines_vars):
        
        #has all the indexes been defined, if so return the result
        if index_x != -1  and index_dx != -1 and index_y != -1 and index_dy != -1:
            return index_x, index_dx, index_y, index_dy

        labale = line_vas[1][0].lower()

        if   labale == labale_X  and index_x  == -1:
            index_x = line_vas[0]
        
        elif labale == labale_dX and index_dx == -1:
            index_dx = line_vas[0]
        
        elif labale == labale_Y  and index_y  == -1:
            index_y = line_vas[0]
        
        elif labale == labale_dY and index_dy == -1:
            index_dy = line_vas[0]
    
     # making shor the the resolt would be retured
    return index_x, index_dx, index_y, index_dy



