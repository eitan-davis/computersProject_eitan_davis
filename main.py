#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

from math import sqrt
from typing import List, Tuple, Callable
from matplotlib import pyplot
#from classes import *
#import parse_row
#import parse_collom
#from extracts import *
#import fitting
#import plot

class PlotPoint2D(object):
    def __init__(self, X:float, dX:float, Y:float, dY:float):# #*args, **kwargs):
        if dX <= 0 or dY <= 0:
            if dX >= 0:
                raise UncertaintyValueError(f"Uncertainty Value Error: uncertainty must be positive number, got 'dY'={dY}")
            if dY >= 0:
                raise UncertaintyValueError(f"Uncertainty Value Error: uncertainty must be positive number, got 'dX'={dX}")

            raise UncertaintyValueError(f"Uncertainty Value Error: uncertainty must be positive number, got 'dX'={dX} and 'dY'={dY}")
        
        self.X  :float = X
        self.dX :float = dX
        self.Y  :float = Y
        self.dY :float = dY


class LengthError(Exception):
    def __init__(self, *args):
        if not args:
            self.args = ("Length error: lists are not the same length.",)


class UncertaintyValueError(Exception):
    def __init__(self, *args):
        if not args:
            self.args = ("Uncertainty Value Error: uncertainty must be positive number",)


def get_file_content(path :str):
    with open(path,'rt') as target:
        return str(target.read())  

LABALE_X  = 'x'
LABALE_dX = 'dx'
LABALE_Y  = 'y'
LABALE_dY = 'dy'
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

# - - row - -

def row_revile_indexes(lines_vars: List[List[str]], labale_X :str = LABALE_X, labale_dX :str = LABALE_dX, labale_Y :str = LABALE_Y, labale_dY :str = LABALE_dY):
    
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


def row_pars_lines(lines_vars: List[List[str]]):
    """
    
    """
    index_x, index_dx, index_y, index_dy = row_revile_indexes(lines_vars)
    
    try:
        dataX  = [float(i) for i in lines_vars[index_x ][1::]]
        datadX = [float(i) for i in lines_vars[index_dx][1::]]
        dataY  = [float(i) for i in lines_vars[index_y ][1::]]
        datadY = [float(i) for i in lines_vars[index_dy][1::]]
    except ValueError as error:
        print("Input file error: Not all values can be convert to numbers")    
    return dataX, datadX, dataY, datadY

# - - collom - -

def collom_pars_lines(lines_vars: List[List[str]]):
    """
    parses the content of the lines into list of X, dX, Y, dY
    """
    
    index_x, index_dx, index_y, index_dy = collom_revile_indexes(lines_vars[0])
    
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


def collom_revile_indexes(first_line_vars :List[str], labale_X :str = LABALE_X, labale_dX :str = LABALE_dX, labale_Y :str = LABALE_Y, labale_dY :str = LABALE_dY):
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

#
def get_data(lines :List[str], labale_X :str = LABALE_X, labale_dX :str = LABALE_dX, labale_Y :str = LABALE_Y, labale_dY :str = LABALE_dY):
    
    #dedect rows or coloms
    mode = identify_rows_or_colloms(lines[0])

    #spit the text from each line
    lines_vars = [line.split() for line in lines ]
    
    dataX  :List[float] = []
    datadX :List[float] = []
    dataY  :List[float] = []
    datadY :List[float] = []

    #extractr the data 
    if mode == "row":
        dataX, datadX, dataY, datadY = row_pars_lines(lines_vars)
    else :
        dataX, datadX, dataY, datadY = collom_pars_lines(lines_vars)
    
    # chek are the lists in the same same length.
    # if not raire LengthError
    if not (len(dataX) == len(datadX) == len(dataY) == len(datadY)):
        raise LengthError

    #orgenis the data in one list of a class PlotPoint2D for ploting and calc chi 2
    points = [PlotPoint2D(dataX[i], datadX[i], dataY[i], datadY[i]) for i in range(len(dataX))]
    
    return points, dataX, datadX, dataY, datadY


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


# - - fitting - -

def get_liniar_fit(points :List[PlotPoint2D] ):
    
    N = len(points)

    dy_2_sum = sum([point.dY**-2 for point in points])
    
    x_wighted_avg  = weighted_average(points, lambda point: point.X, dy_2_sum)
    y_wighted_avg  = weighted_average(points, lambda point: point.Y, dy_2_sum)
    xy_wighted_avg = weighted_average(points, lambda point: point.X * point.Y, dy_2_sum)
    x2_wighted_avg = weighted_average(points, lambda point: point.X**2, dy_2_sum)
    y2_wighted_avg = weighted_average(points, lambda point: point.Y**2, dy_2_sum)
    dy_wighted_avg = weighted_average(points, lambda point: point.dY**2, dy_2_sum)

    a = (xy_wighted_avg - x_wighted_avg*y_wighted_avg) / (x2_wighted_avg - x_wighted_avg**2)
    
    da = (dy_wighted_avg / (N * (x2_wighted_avg - x_wighted_avg**2)))**0.5
    
    b = y_wighted_avg - a * x_wighted_avg
    
    db = (dy_wighted_avg * x2_wighted_avg / (N *(x2_wighted_avg - x_wighted_avg**2) ))**0.5

    return a, da, b, db, N


def weighted_average(points :List[PlotPoint2D], func :Callable[[PlotPoint2D],float], dy_2_sum :float = 0.0):
    if dy_2_sum > 0:
        return float(sum([(func(point) / point.dY**2) for point in points]) / dy_2_sum)
    else :
        return float(sum([(func(point) / point.dY**2) for point in points]) / sum([point.dY**-2 for point in points]))


def calc_chi_2_liniar(points :List[PlotPoint2D], a :float, b :float):
    """
    calculates chi^2 for liniar fit assumint that dy>>dx
    """
    return sum([( (point.Y - (a * point.X + b)) / (point.dY) )**2 for point in points])


def calc_chi_2(points :List[PlotPoint2D], a :float, b :float,
               function :Callable[[float,float,float], float] = (lambda x, m, n: (x * m + n))):
    """
    calculates chi^2 for any funtion 
    """
    
    return float(sum([( (point.Y - function(point.X, a, b)) /
                        ((point.dY**2 + (function(point.X + point.dX, a, b) - function(point.X - point.dX, a, b))**2)**0.5) )**2 
                        for point in points]))


# - - plot - -

def plot_data_and_fit(dataX :List[float], datadX :List[float], dataY :List[float], datadY :List[float], 
                      a :float, b :float, labelX:str, labelY :str, 
                      file_name :str = 'linear_fit', plot_format :str='svg'):
    
    pyplot.plot( dataX, [a * x + b for x in dataX], 'red')
    
    pyplot.errorbar(x=dataX, y=dataY, yerr = datadY, xerr=datadX, fmt='none', ecolor='b')

    pyplot.ylabel(labelY)
    
    pyplot.xlabel(labelX)

    if file_name:
        pyplot.savefig(fname = file_name, format = plot_format)
    else:
        pyplot.show()
    
    pyplot.gcf().clear()

    

def plot_simple_graph(dataX :List[float], dataY :List[float], labelX:str = 'a', labelY :str = 'chi2(a,b)',
                      file_name :str = 'numeric_sampling', plot_format :str='svg', plot_color :str= 'blue'):
    
    pyplot.plot(dataX, dataY, plot_color)
    
    pyplot.xlabel(labelX)
    
    pyplot.ylabel(labelY)
    
    if file_name:
        pyplot.savefig(fname = file_name, format = plot_format)
    else:
        pyplot.show()
    
    pyplot.gcf().clear()



def fit_linear(path: str):
    
    # get the file content and split it into lines
    lines :List[str] = [line for line in (get_file_content(path = path)).split('\n')]
    
    # remove begining empty or spase only lines
    for element in enumerate(lines):
        if element[1].replace(' ','')=='':
            lines.pop(0)
        break

    try:
        points, dataX, datadX, dataY, datadY = get_data(lines)
    except UncertaintyValueError as error:
        print("Input file error: Not all uncertainties are positive.")
        return
    except LengthError as error:
        print("Input file error: Data lists are not the same length.")
        return
    except Exception as error:
        print(error)
        return
    labelX, labelY = extract_headers(lines)
    
    a, da, b, db, N = get_liniar_fit(points)

    chi2 = calc_chi_2_liniar(points, a, b)

    chi2_reduced  = chi2 / (N - 2)

    print(f"a = {a} +- {da}",end = '\n\n')
    print(f"b = {b} +- {db}",end = '\n\n')
    print(f"chi2 = {chi2}",end = '\n\n')
    print(f"chi2_reduced = {chi2_reduced}")

    plot_data_and_fit(dataX, datadX, dataY, datadY, a, b, labelX, labelY)


def arange(start :float, stop :float, step :float = 1.):
    if start == stop:
        return [start]
    if step == 0:
        raise ValueError("step cannot be zero")
    step = abs(step) if start < stop else -abs(step)
    
    fixer_fractions = int(1/step) * 4
    arr = []
    
    for i in range(0, int(abs((stop-start)/step)+1)):
        #
        arr.append((start * fixer_fractions +  i * (step * fixer_fractions))/fixer_fractions)
        i += 1
    
    return arr


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


def search_best_parameter(path :str):
    
    # get the file content and split it into lines
    lines :List[str] = [line for line in (get_file_content(path = path)).split('\n')]
    # remove begining empty or spase only lines
    for element in enumerate(lines):
        if element[1].replace(' ','')=='':
            lines.pop(0)
        break

    try:
        points, dataX, datadX, dataY, datadY = get_data(lines)
        paramA, paramB = extract_parms_to_fit(lines)
        ListParamA = arange(paramA['start'], paramA['end'], paramA['step'])
        ListParamB = arange(paramB['start'], paramB['end'], paramB['step'])
    except UncertaintyValueError as error:
        print("Input file error: Not all uncertainties are positive.")
        return
    except LengthError as error:
        print("Input file error: Data lists are not the same length.")
        return
    except Exception as error:
        print(error)
        return
    
    axisX, axisY = extract_headers(lines)

    bestA, bestB = ListParamA[0], ListParamB[0]
    
    best_chi2 = calc_chi_2(points,bestA,bestB)
    
    for i in ListParamA:
        for j in ListParamB:
            temp_chi2 = calc_chi_2(points, i, j)
            if temp_chi2 <= best_chi2:
                best_chi2 = temp_chi2
                bestA, bestB = i, j
    
    chi2_reduced = best_chi2 / (len(points) - 2)

    print(f"a = {bestA} +- {paramA['step']}", end = '\n\n')
    print(f"b = {bestB} +- {paramB['step']}", end = '\n\n')
    print(f"chi2 = {best_chi2}", end = '\n\n')
    print(f"chi2_reduced = {chi2_reduced}", end = '\n')

    plot_data_and_fit(dataX, datadX, dataY, datadY, bestA, bestB, axisX, axisY)

    plot_simple_graph(ListParamA, [calc_chi_2(points,varA,bestB) for varA in ListParamA], labelY=f'chi2(a, b = {bestB:.2f})')
