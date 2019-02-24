#!/usr/bin/python3
import math

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


# - - - - -

class InputError(Exception):
    def __init__(self, *args):
        pass
        #super(InputError,Exception).__init__(*args))


class param (object):
    def  __init__ (self,value:float, error: float):
        if error < 0:
            raise ValueError(f"error value must be positive got {error}")
        self.value = value
        self.error = error
    
    def __add__ (self, other):
        if type(other) == param:
            return param(self.value + other.value, math.sqrt(self.error**2 + other.error**2))
        
        elif type(other) == int or type(other) == float:
            return param(value=self.value + other, error=self.error)
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'param' and '{type(other)}'")
    
    
    def __eq__(self, value):
        if hasattr(value,'value') and hasattr(value,'error'):
            return False
        return True if self.value == value.value and self.error == value.error else False
    
    
    def has_error(self):
        return True if self.error > 0 else False
