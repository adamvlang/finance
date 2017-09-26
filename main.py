import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np

def calcDir(dates, values):
    """
    This is a function for calculating the angular coefficient between two points.
    INPUT
    values - a list of points [x, y]
    OUTPUT
    k - a list of the k-values
    """
    print("Calculating k-values")
    k = []
    k_dates = []
    k_points = []
    for i in range(len(values)-1):
        "try-except to handle one-of errors"
        if i < (len(values)-1):
            t2 = (dates[i+1] - dates[i]).days
            t1 = values[i+1] - values[i]
            k.append(float(t1)/float(t2))
            k_dates.append(dates[i])
            k_points.append(values[i])
    print("k-values done!")
    return k, k_dates, k_points

def extrema(values, ex_type):
    """
    Function for finding extreme points, iterates through and finds where f'(x) = 0 for maximas and minimis.
    INPUT
    values - a list of points
    ex_type - str with "max" or "min" for desired type
    OUTPUT

    """
    print("Calculating extremas")
    exas = []
    idx = []
    if ex_type == "min":
        for i,j in enumerate(values):
            if i > 0 and i < (len(values)-1):
                if j < values[i-1] and j < values[i+1]:
                    exas.append(j)
                    idx.append(i)
    elif ex_type == "max":
        for i,j in enumerate(values):
            if i > 0 and i < (len(values)-1):
                if j > values[i-1] and j > values[i+1]:
                    exas.append(j)
                    idx.append(i)
    elif ex_type == "sdl_min":
        for i,j in enumerate(values):
            if i > 0 and i < (len(values)-1):
                if j < 0 and values[i+1] > 0 :
                    exas.append(j)
                    idx.append(i+1)
    else:
        raise NameError('Only a string with "max" and "min" is usable as extrema type')
        return
    print("Extremas done!")
    return idx, exas    

def calAng(dates, values):
    """
    Calculates the two most defining points and the angle between them.
    """
    print("Calculating the most defing points and angle")
    k, k_dates, k_points = calcDir(dates, values)
    while len(k_points) > 3:
        idx, minima = extrema(k, "sdl_min")
        if len(idx) < 2:
            k_points = [dir_points[0], dir_points[-1]]
            k_dates = [dir_dates[0], dir_dates[-1]]
            k, k_d, k_p = calcDir(k_dates, k_points)
            break
        dir_dates = [k_dates[i] for i in idx]
        dir_points = [k_points[i] for i in idx]
        k, k_dates, k_points = calcDir(dir_dates, dir_points)
    print("Def angles and points done!")
    return k_dates, k_points, k[0]

def calcOBV(f):
    print("Calculating OBV")
    OBV = [[f.ix[1].name.date(), f['Volume'][1]]]

    for i,j in enumerate(f['Close']):
        if i > 0:
            if j > f['Close'][i-1]:
                OBV.append([f.ix[i].name.date(), (f['Volume'][i] + OBV[-1][1])])
            else:
                OBV.append([f.ix[i].name.date(), -f['Volume'][i] + OBV[-1][1]])
    print("OBV done!")
    return OBV

def close_lst(f):
    print("Calculating closing price!\n")
    close_price = []
    for i,j in enumerate(f['Close']):
        close_price.append([f.ix[i].name.date(), f['Close'][i]])
    print("Closing price done!")
    return close_price

def angle(values, angle_type):
    print("Running show!")
    min_days = []
    max_days = []
    min_idx, minimas = extrema([row[1] for row in values], "min")
    max_idx, maximas = extrema([row[1] for row in values], "max")
    print(minimas)
    print("show extras done")
    if angle_type == "min":
        for i in range(len(min_idx)):
            min_days.append(values[min_idx[i]][0])
        def_dates, def_point, k = calAng(min_days, minimas)
    if angle_type == "max":
        for i in range(len(max_idx)):
            max_days.append(values[max_idx[i]][0])
    print("Show done!")
    return def_dates, def_point, k

def trend_indicator(k, point, date, f): 
    today = f['Close'][-1]
    elapsed = (dt.date.today() - date).days
    print(point+(elapsed*k))
    print(today)
    if (elapsed*k)+point > today:
        return True
    else:
        return False
      
"Setting up time frame for analysis"
end = dt.date.today()
start = end - dt.timedelta(days=183)

f = web.DataReader("AAPL", 'yahoo', start, end)

obv = calcOBV(f)
close = close_lst(f)
def_dates, def_point, k = angle(close, "min")
indicator = trend_indicator(k, def_point[-1], def_dates[-1], f)

print(indicator)
print(k)
print(def_point)
print(def_dates)
print("done!")
