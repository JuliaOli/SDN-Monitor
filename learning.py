#influx -database 'database_name' -execute 'SELECT * FROM table_name' -format csv > test.csv


# Load the Pandas libraries with alias 'pd' 
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

data =  pd.read_csv("db/influx_database.csv")

devices = list(set(data['device']))
devices_time = pd.to_datetime(data['time'], unit='ms')

print(devices_time)

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