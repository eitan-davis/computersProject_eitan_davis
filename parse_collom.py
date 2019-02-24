#!/usr/bin/python3

from typing import List
from classes import LengthError

labale_X = 'x'
labale_dX = 'dx'
labale_Y = 'y'
labale_dY = 'dy'


def pars_lines(lines_vars: List[List[str]]):#, flag :bool=False):#->List[float]:
    """
    parses the content of the lines into list of X, dX, Y, dY
    """
    
    index_x, index_dx, index_y, index_dy = revile_indexes(lines_vars[0])
    
    if len(lines_vars)==1:
        raise Exception("Input file error: no data in the file")
    
    dataX, datadX, dataY, datadY = [], [], [], []

    for i in range(len(lines_vars)-1):    
        elements = lines_vars[i+1]
        
        #chek is the list of numbers ended 
        if elements == [] or elements == [''] or not elements[0].isnumeric():
            break
        #chek are 
        if len(elements)<4:
            raise LengthError(f"not enough numbers in line {i} of the content")

        dataX.append( float(elements[index_x]))
        datadX.append(float(elements[index_dx]))
        dataY.append( float(elements[index_y]))
        datadY.append(float(elements[index_dy]))
    
    return dataX, datadX, dataY, datadY
        


def revile_indexes(first_line_vars :List[str]):
    index_x, index_dx, index_y, index_dy = -1, -1, -1, -1

    for element in enumerate(first_line_vars):
        
        var = str(element[1]).lower()
        
        if   var == labale_X:
            index_x =  element[0]
        
        elif var == labale_dX:
            index_dx = element[0]
        
        elif var == labale_Y:
            index_y =  element[0]
        
        elif var == labale_dY:
            index_dy = element[0]

    return index_x, index_dx, index_y, index_dy      