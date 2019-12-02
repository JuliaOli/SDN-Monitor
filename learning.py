#influx -database 'database_name' -execute 'SELECT * FROM table_name' -format csv > test.csv


# Load the Pandas libraries with alias 'pd' 
import pandas as pd 
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
data =  pd.read_csv("/home/mariajulia/Documentos/Github_repo/SDN-Monitor/db/influx_database.csv", delimiter = ';')
print(data)
# Preview the first 5 lines of the loaded data 