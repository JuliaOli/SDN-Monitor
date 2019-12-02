#influx -database 'database_name' -execute 'SELECT * FROM table_name' -format csv > test.csv


# Load the Pandas libraries with alias 'pd' 
import pandas as pd 
import numpy as np
import seaborn
import matplotlib.pyplot as plt


data =  pd.read_csv("/home/mariajulia/Documentos/Github_repo/SDN-Monitor/db/influx_database.csv", delimiter = ';')
#https://machinelearningmastery.com/load-explore-time-series-data-python/
#https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.Series.from_csv.html
ts = pd.Series(data, index=pd.date_range(start="2014-02-01", periods=n, freq="H"))


fig, ax = plt.subplots(figsize=(12,5))
seaborn.boxplot(ts.index.dayofyear, ts, ax=ax)
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 

# Preview the first 5 lines of the loaded data 