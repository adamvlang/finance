import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np


class Stock:
    
    def __init__(self, start, end, symbol, trade):
        self.stock_data = web.DataReader(symbol, 'yahoo', start, end)
        self.type = None
        setType()
        self.obv_trend = self.calcObv(self.stock_data)
        
    def setType(self):
        if trade == "sell":
            self.type = "min"
        elif trade == "buy":
            self.type = "max"
        else:
            raise NameError("Must by or sell")

    def calcDir(self, dates, values):
        """
        This is a function for calculating the angular coefficient between two points.
        INPUT
            values -    a [n x 1] list of points the points
            dates -     a [n x 1] list of the dates
        OUTPUT
            k -         a [m x 1] list containing the k-values
        """
        print("k-values running...")
        k = []
        k_dates = []
        k_points = []
        for i in range(len(values)-1):
            if i < (len(values)-1):
                t2 = (dates[i+1] - dates[i]).days
                t1 = values[i+1] - values[i]
                k.append(float(t1)/float(t2))
                k_dates.append(dates[i])
                k_points.append(values[i])
        print("k-values done!")
        return k, k_dates, k_points

    def extrema(self, values, ex_type):
        """
        Function for finding extreme points, iterates through and finds where f'(x)
        = 0 for maximas and minimis.
        INPUT
            values -    a [n x 1] list of points
            ex_type -   a "str" with the frase of the type of point that is wanted
        OUTPUT
            idx -       a [m x 1] list of indexes of [values] that are the extreme points
            exas -      a [m x 1] list with the extreme points
        """
        print("Extremas running...")
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
        elif ex_type == "min_k":
            for i,j in enumerate(values):
                if i < (len(values)-1):
                    if j < values[i+1]:
                        exas.append(j)
                        idx.append(i+1)
        elif ex_type == "max_k":
            for i,j in enumerate(values):
                if i < (len(values)-1):
                    if j > values[i+1]:
                        exas.append(j)
                        idx.append(i+1)
        else:
            raise NameError('Incorrect type as input in extremat')
            return
        print("Extremas done!")
        return idx, exas    

    def calAng(self, dates, values, angle_type):
        """
        This function will calculate the most defining points and calculate the k-value between them.
        INPUT
            values -        a [n x 1] list containing the values used for analasys,
                            could be close, obv etc.
            dates -         a [n x 1] list containing the corresponding dates for values.
        OUTPUT
            k_dates -       a [2 x 1] list containin the dates that def. the direction of the graph
            k_points -      a [2 x 1] list containging th points that defines the direction of the graph
            k[0] -          the scalar k-value that defines the line
        """
        print("Defining points running...")
        #Determining the type of extrema value to be calculated
        if angle_type == "max":
            type_k = "max_k"
        elif angle_type == "min":
            type_k = "min_k"
        else:
            raise NameError('Incorrect type as angle type')
            return

        #Initial values
        k, k_dates, k_points = self.calcDir(dates, values)

        #While there is a maximum left
        while len(k_points) > 3:
            idx, minima = self.extrema(k, type_k)
            #When the function is done we need the most defining points 
            if len(idx) < 3:
                k_points = [dir_points[0], dir_points[-1]]
                k_dates = [dir_dates[0], dir_dates[-1]]
                k, k_d, k_p = self.calcDir(k_dates, k_points)
                break
            dir_dates = [k_dates[i] for i in idx]
            dir_points = [k_points[i] for i in idx]
            k, k_dates, k_points = self.calcDir(dir_dates, dir_points)
        print("Defining points done!")
        return k_dates, k_points, k[0]

    def angle(self, dates, values, angle_type):
        """
        This function will calculate the most defining points and calculate the k-value between them.
        INPUT
            dates -         a [n x 1] list containing the dates used for analysis
            values -        a [n x 1] list containing the values used for analysis
                            could be close, obv etc.
            angle_type -    a "str" defining what type of angle the function should look for, on top
                            of the graph or below. 
        OUTPUT
            def_dates -     a [m x 1] list with the dates that defines the line
            def_points -    a [m x 1] list with the points that define the line
            k -             a [m x 1] list with the k-value that defines the line
        """
        
        print("Angels running...")
        exa_days = []
        exa_idx, extms = self.extrema(values, angle_type)
        for i in range(len(exa_idx)):
            exa_days.append(dates[exa_idx[i]])
        def_dates, def_point, k = self.calAng(exa_days, extms, angle_type)
        print("Angles done!")
        return def_dates, def_point, k

    def calcObv(self, f):
        """
        Creates a list of all the obv values for the stock in f.
        INPUT
            f - the pandas object of the current stock
        OUTPUT
            obv - a [n x n] list [date, obv] of the obv values and the corresponding dates
        """
        print("obv running...")
        obv = [f['Volume'][1]]
        dates = [f.ix[1].name.date()]

        for i,j in enumerate(f['Close']):
            if i > 0:
                if j > f['Close'][i-1]:
                    dates.append(f.ix[i].name.date())
                    obv.append(f['Volume'][i] + obv[-1])
                else:
                    dates.append(f.ix[i].name.date())
                    obv.append(-f['Volume'][i] + obv[-1])
        def_dates, def_points, k = self.angle(dates, obv, self.type)
        return k
        print("obv done!")

    def close_lst(self, f):
        """
        Creates a list of all the closing prices in f.
        INPUT
            f - the pandas object of the current stock
        OUTPUT
            close_price - a [n x 1] the closing prices of the stock in a list
        """
        print("Closing price running...")
        close_price = []
        dates = []
        for i,j in enumerate(f['Close']):
            close_price.append(f['Close'][i])
            dates.append(f.ix[i].name.date())
        print("Closing price done!")
        return dates, close_price

    def trend_indicator(self, k, point, date, clos): 
        """
        The trend inducator will give a bool considering if a stock should be sold
        INPUT
            k - scalar k-value calculated on the specific time period
            point - scalar point closes to the current closing price
            date - timedate object with date on the point closes to the current
            clos - scalar closing prise of today
        OUTPUT
            True/False if the stock have passed the estimated price
        """
        print("Trend indicator running...")
        today = f['Close'][-1]
        elapsed = (dt.date.today() - date).days
        if (elapsed*k)+point > today:
            print("Trend indicator done!")
            return True
        else:
            print("Trend indicator done!")
            return False

"Setting up time frame for analysis"
end = dt.date.today()
start = end - dt.timedelta(days=183)

st = Stock(start, end, "MOB.ST", "sell")
print(st.obv_trend)

print("done!")
