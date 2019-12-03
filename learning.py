#influx -database 'database_name' -execute 'SELECT * FROM table_name' -format csv > test.csv


# Load the Pandas libraries with alias 'pd' 
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

data =  pd.read_csv("db/influx_database.csv")

devices_time = []
# map returns Generator (remap an array into other) -> list convert generator to array
# replace zeros in the end of the time transform the timestamp into datetime
devices_time = list(map(lambda it: str(it).replace('000000000',''), data['time']))
tempos = pd.to_datetime(devices_time, unit='s')


#for time in data['time'].values:
#    time = str(time).replace('000000000', '')
#    devices_time.append(pd.to_datetime(time, unit='ms'))
#    print(time)


#Data value plot according to time
data[:200].boxplot(by='time', 
                column=['value'], 
                grid=False)

plt.show()


#bplot = sns.boxplot(y='lifeExp', x='continent', 
                 #data= data['value'][:100], 
                 #width=0.5,
                 #palette="colorblind")

#http://cmdlinetips.com/2018/03/how-to-make-boxplots-in-python-with-pandas-and-seaborn/
#https://www.inf.ufsc.br/~marcelo.menezes.reis/Cap4.pdf