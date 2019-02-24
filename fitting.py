#!/usr/bin/python3

import typing
import re
import math
import cmath
from math import sqrt
from typing import List, Tuple, Callable
from classes import *
import parse_row
import parse_collom


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
    
    da = math.sqrt(dy_wighted_avg / (N * (x2_wighted_avg - x_wighted_avg**2)))
    
    b = y_wighted_avg - a * x_wighted_avg
    
    db = math.sqrt(dy_wighted_avg * x2_wighted_avg / (N *(x2_wighted_avg - x_wighted_avg**2) ))

    return a, da, b, db, N


def weighted_average (points :List[PlotPoint2D], func :Callable[[PlotPoint2D],float], dy_2_sum :float = 0.0):
    if dy_2_sum > 0:
        return float(sum([(func(point) / point.dY**2) for point in points]) / dy_2_sum)
    else :
        return float(sum([(func(point) / point.dY**2) for point in points]) / sum([point.dY**-2 for point in points]))


def average (*lst):
    return sum(lst) / len(lst)


def calc_chi_2_liniar (points :List[PlotPoint2D], a :float, b :float):
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
                        (sqrt(point.dY**2 + (function(point.X + point.dX, a, b) - function(point.X - point.dX, a, b))**2)) )**2 
                        for point in points]))
