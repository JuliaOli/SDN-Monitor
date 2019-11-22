#influx -database 'database_name' -execute 'SELECT * FROM table_name' -format csv > test.csv
# Load the Pandas libraries with alias 'pd' 
import pandas as pd 
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
data = pd.read_csv("influx_database.csv") 
# Preview the first 5 lines of the loaded data 