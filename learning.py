#influx -database 'database_name' -execute 'SELECT * FROM table_name' -format csv > test.csv


# Load the Pandas libraries with alias 'pd' 
import pandas as pd 
import numpy as np
import seaborn
import matplotlib.pyplot as plt

data =  pd.read_csv("db/influx_database.csv")
#https://machinelearningmastery.com/load-explore-time-series-data-python/
#https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.Series.from_csv.html

devices = list(set(data['device']))

#fig, ax = plt.subplots(figsize=(12,5))
#seaborn.boxplot(ts.index.dayofyear, ts, ax=ax)
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 

# Preview the first 5 lines of the loaded data 