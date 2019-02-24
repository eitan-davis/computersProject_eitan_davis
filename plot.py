#!/usr/bin/python3


from matplotlib import pyplot
from typing import List as List



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





    



