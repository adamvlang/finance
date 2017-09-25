import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np

def calcDir(values):
    """
    This is a function for calculating the angular coefficient between two points.
    INPUT
    values - a list of points [x, y]
    OUTPUT
    k - a list of the k-values
    """
    k = []
    for i in range(len(values)):
        "try-except to handle one-of errors"
        if i < (len(values)-1):
            t2 = (values[0][i+1] - values[0][i]).days
            t1 = values[1][i+1] - values[1][i]
            k.append(float(t1)/float(t2))
    return k
def extrema(values, ex_type):
    """
    Function for finding extreme points, iterates through and finds where f'(x) = 0 for maximas and minimis.
    INPUT
    values - a list of points
    ex_type - str with "max" or "min" for desired type
    OUTPUT

    """
    exas = []
    idx = []
    if ex_type == "min":
        for i,j in enumerate(values):
            if i > 0 and i < (len(values)-1):
                if j > values[i-1] and j > values[i+1]:
                    exas.append(j)
                    idx.append(i)
    elif ex_type == "max":
        for i,j in enumerate(values):
            if i > 0 and i < (len(values)-1):
                if j < values[i-1] and j < values[i+1]:
                    exas.append(j)
                    idx.append(i)
    else:
        raise NameError('Only a string with "max" and "min" is usable as extrema type')
        return
    return idx, exas    

def calAng(dates, values):
    """
    Calculates the two most defining points and the angle between them.
    """
    val_temp = []
    values = calcDir([dates, values])
    print(values)
    while len(values) > 2:
        idx, values = extrema(values, "min")
        for i in range(len(idx)):
            val_temp.append(values[i][0])
        values = val_temp
    return idx, values

"Setting up time frame for analysis"
end = dt.date.today()
start = end - dt.timedelta(days=183)

maximas = []
minimas = []
obv_min_days = []
obv_max_days = []
f = web.DataReader("MOB.ST", 'yahoo', start, end)
OBV = [[f.ix[1].name.date(), f['Volume'][1]]]

for i,j in enumerate(f['Close']):
    if i > 0:
        if j > f['Close'][i-1]:
           OBV.append([f.ix[i].name.date(), (f['Volume'][i] + OBV[-1][1])])
        else:
            OBV.append([f.ix[i].name.date(), -f['Volume'][i] + OBV[-1][1]])
obv_min_idx, obv_min = extrema([row[1] for row in OBV], "min")
obv_max_idx, obv_max = extrema([row[1] for row in OBV], "max")
for i in range(len(obv_min_idx)):
    obv_min_days.append(OBV[obv_min_idx[i]][0])
for i in range(len(obv_max_idx)):
    obv_max_days.append(OBV[obv_max_idx[i]][0])
idx, def_point = calAng(obv_min_days, obv_min)
print(def_point)
print("done!")
