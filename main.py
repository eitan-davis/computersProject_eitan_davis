#!/usr/bin/python3.7

from typing import List
from classes import *
import parse_row
import parse_collom
from extracts import *
import fitting
import plot

def get_file_content(path :str):
    with open(path,'rt') as target:
        return str(target.read())  


#the main common code for both functions
#
def get_data(lines :List[str]):
    
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
        dataX, datadX, dataY, datadY = parse_row.pars_lines(lines_vars)
    else :
        dataX, datadX, dataY, datadY = parse_collom.pars_lines(lines_vars)
    
    # chek are the lists in the same same length.
    # if not raire LengthError
    if not (len(dataX) == len(datadX) == len(dataY) == len(datadY)):
        raise LengthError

    #orgenis the data in one list of a class PlotPoint2D for ploting and calc chi 2
    points = [PlotPoint2D(dataX[i], datadX[i], dataY[i], datadY[i]) for i in range(len(dataX))]
    
    return points, dataX, datadX, dataY, datadY


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
    
    a, da, b, db, N = fitting.get_liniar_fit(points)

    chi2 = fitting.calc_chi_2_liniar(points, a, b)

    chi2_reduced  = chi2 / (N - 2)

    print(f"a = {a} +- {da}",end = '\n\n')
    print(f"b = {b} +- {db}",end = '\n\n')
    print(f"chi2 = {chi2}",end = '\n\n')
    print(f"chi2_reduced = {chi2_reduced}")

    plot.plot_data_and_fit(dataX, datadX, dataY, datadY, a, b, labelX, labelY)

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
    
    best_chi2 = fitting.calc_chi_2(points,bestA,bestB)
    
    for i in ListParamA:
        for j in ListParamB:
            temp_chi2 = fitting.calc_chi_2(points, i, j)
            if temp_chi2 <= best_chi2:
                best_chi2 = temp_chi2
                bestA, bestB = i, j
    
    chi2_reduced = best_chi2 / (len(points) - 2)

    print(f"a = {bestA} +- {paramA['step']}", end = '\n\n')
    print(f"b = {bestB} +- {paramB['step']}", end = '\n\n')
    print(f"chi2 = {best_chi2}", end = '\n\n')
    print(f"chi2_reduced = {chi2_reduced}", end = '\n')

    plot.plot_data_and_fit(dataX, datadX, dataY, datadY, bestA, bestB, axisX, axisY)

    plot.plot_simple_graph(ListParamA, [fitting.calc_chi_2(points,varA,bestB) for varA in ListParamA], labelY=f'chi2(a, b = {bestB:.2f})')





