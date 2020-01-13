#influx -database 'database_name' -execute 'SELECT * FROM table_name' -format csv > test.csv

#http://cmdlinetips.com/2018/03/how-to-make-boxplots-in-python-with-pandas-and-seaborn/
#https://www.inf.ufsc.br/~marcelo.menezes.reis/Cap4.pdf

# Load the Pandas libraries with alias 'pd' 
import pandas as pd
import numpy as np
import seaborn as sns

from pandas import read_csv
from pandas import datetime
from pandas.plotting import autocorrelation_plot
from pandas import DataFrame

from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA

data =  read_csv("/home/mj/Documentos/Git Lab repositories/Version_control_backup/Git/SDN-Monitor/db/influx_database.csv")

devices_time = []
# map returns Generator (remap an array into other) -> list convert generator to array
# replace zeros in the end of the time transform the timestamp into datetime
devices_time = list(map(lambda it: str(it).replace('000000000',''), data['time']))
tempos = pd.to_datetime(devices_time, unit='s')

print(tempos[1])

data.plot()
pyplot.show()

#plots the autocorrelation for a large number of lags in the time series.
autocorrelation_plot(data[:200])
pyplot.show()
