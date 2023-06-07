import pandas_datareader as pdr
import numpy as np
import datetime
import bisect
from config import *
from apikey import *
from flask import Flask, render_template
class risknreward:
    def getTrades(self, data:str, remoterefresh:bool) -> np.array:
        filename = "trades.csv"
        pnl = np.array([])
        try:
            pnl = np.loadtxt(filename, delimiter=",")
            if debug and 1+1 == 3:
                print("Trades array: ")
                print(pnl)
                print("Array size: %d " % (pnl.size))
        except Exception as e:
            print("Error occurred while reading the file:")
            print(e)

        if data == "remote" and (pnl.size == 0 or remoterefresh): 
            start_date = datetime.datetime.strptime(fromdate, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(todate, '%Y-%m-%d')
            qt = pdr.DataReader(issue, data_source, start_date, end_date,api_key=apikey)
            
            if debug and 1+1 == 3: #print result
                print (qt.shape)
                print (qt.head())
                nrows = qt.shape[0]
                print ("Number Rows: %d " % (nrows))
            
            qtC = np.array(qt.close)
            #pnl = np.diff(qtC)
            pnl = (qtC[1:] - qtC[:-1]) / qtC[:-1]     
            np.savetxt(filename, pnl, fmt="%f", delimiter=",")
                    
        return pnl
    
    def calCAR(self, pnl:np.array) -> dict:
        nrand = 100
        dd95_limit = 0.10 # drawdown limit at 5% risk
        randreplace = True
        adaptive = True
        fractionstep = 2
        fractionlimt = 401
        accuracy_tolerance = 0.05 # default 5% risk tolerance
        twr25 = list()
        ddlist = list()
        count = pnl.size
        if count == 0:
            return False

        f = 0
        prodd = 0
        if adaptive:
            exhaustive = lambda x: x < accuracy_tolerance
        else:
            exhaustive = lambda x: True and f < fractionlimt
        while exhaustive(prodd):
            twr = list()
            countdd =0
            f += fractionstep
            data = list()
            for iseq in range(nrand): # loop over # of random sequences
                # Randomly reorder trades             
                randtrades = np.random.RandomState(seed=None).choice(pnl,size=count,replace=randreplace)
                # Calculate account balance and drawdown for current sequence of trades
                equity = 1
                equityhigh = equity
                ddmax = 0
                line = [1]         
                for i in range(count):
                    newequity = equity * (1+(f/100*(randtrades[i])))
                    
                    # Calculate closed trade percent drawdown
                    if (newequity > equityhigh):
                        equityhigh = newequity
                    else:
                        dd = (equityhigh - newequity) / equityhigh
                        if (dd > ddmax):
                            ddmax = dd
                    equity = newequity
                    line.append(equity)
                    
                # Accumulate results for probability calculations
                twr.append(equity)
                if ddmax > dd95_limit:
                    countdd += 1
                safef = f
                data.append(line)
                if debug and 1+1 == 3: #print result
                    print ("ddmax: ", ddmax,"countdd: ", countdd,"f: ", f,)
            
            twr25.append(np.percentile(twr,25))
            prodd = countdd / nrand
            ddlist.append(prodd)
            if debug and 1+1 == 3: #print result
                print ("twr: ", twr)
            #np.savetxt("debug.csv", twr, fmt="%f", delimiter=",")

        start_date = datetime.datetime.strptime(fromdate, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(todate, '%Y-%m-%d')            
        time_delta = end_date - start_date
        days = time_delta.days
        # Calculate the number of years by dividing the number of days by 365 (approximation)
        years_in_hist = days / 365
        if debug and 1+1 == 3: #print result
            print ("years_in_hist: ", years_in_hist) 
                                  
        safef_index = bisect.bisect_left(ddlist, accuracy_tolerance)
        if safef_index > len(twr25) - 1:
            safef_index = len(twr25) - 1
        car25 = (twr25[safef_index] ** (1/years_in_hist) - 1) * 100
        if debug and 1+1 == 3: #print result
            print ("twr25: ", twr25[safef_index]-1)
            
        # calculate base eq curve
        return {'safef':safef,'car25':car25,'eq':data}
    
app = Flask(__name__)
@app.route('/eq')
def chart():
   
    # Generate data for each line  
    pnl = risknrewardtest.getTrades(datasource,remoterefresh)
    result = risknrewardtest.calCAR(pnl)
    num_lines = 3
    labels = list(range(1, pnl.size+1))
    data = []
    for i in range(num_lines):
        line_data = result['eq'][i]
        data.append(line_data)
        if debug and 1+1 == 3: #print result
            print ("line_data: ", line_data)          
 
    # Return the components to the HTML template
    return render_template(
        template_name_or_list='chartjs.html',
        data=data,
        labels=labels,
        num_lines=num_lines
    )

@app.route('/', methods=['GET', 'POST'])
def hello():
    head = f"Stock: {issue}<br>Periods: {fromdate} to {todate}"
    return f"{head}<br>Fixed Fraction(%): {result['safef']:.1f}, CAR25(%): {result['car25']:.3f}"
    
if __name__ == '__main__':
    risknrewardtest =  risknreward()
    datasource = "remote"
    remoterefresh = False
    pnl = risknrewardtest.getTrades(datasource,remoterefresh)
    #print("pnl is ", pnl) # Output: list of pnl
    
    result = risknrewardtest.calCAR(pnl)
    #print(f"Fixed Fraction(%): {result['safef']:.1f}, CAR25(%): {result['car25']:.3f}")
    
    app.run()