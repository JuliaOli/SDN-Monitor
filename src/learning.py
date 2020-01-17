#influx -database 'database_name' -execute 'SELECT * FROM table_name' -format csv > test.csv

#http://cmdlinetips.com/2018/03/how-to-make-boxplots-in-python-with-pandas-and-seaborn/
#https://www.inf.ufsc.br/~marcelo.menezes.reis/Cap4.pdf
#https://towardsdatascience.com/the-akaike-information-criterion-c20c8fd832f2
#
#
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

class LearningTest:
    def __init__(self, dataAdress):
        self.data = dataAdress
        # data =  read_csv("/home/mj/Documentos/Git Lab repositories/Version_control_backup/Git/SDN-Monitor/db/influx_database.csv")
  
    def autocorrelation_plots(self, data):
        plot_acf(series)
        plot_pacf(series)
        pyplot.show()

    def residuals_plots(self, model_fit):
        # Residual of an observed value is the difference between the observed value 
        # and the estimated value of the quantity of interest (for example, a sample mean).
        # After the fitting the model we can obtain our residuals and visualize them
        # Model_fit can be any model class, ex.: ARIMA.
        residuals = DataFrame(model_fit.resid) # Residuals from our model
        residuals.plot()
        pyplot.show()
        # Generate Kernel Density Estimate plot using Gaussian kernels.
        residuals.plot(kind='kde')
        pyplot.show()
        print(residuals.describe())
    
    def predictions_plots(self, test, predictions):
        # A line plot is created showing the expected values (blue) 
        # compared to the rolling forecast predictions (red). 
        # We can check if the values show some trend and are in the correct scale.
        pyplot.plot(test)
        pyplot.plot(predictions, color='red')
        pyplot.show()

    
    def parser_influx_data(self, data):
        devices_time = []
        # map returns Generator (remap an array into other) -> list convert generator to array
        # replace zeros in the end of the time transform the timestamp into datetime
        devices_time = list(map(lambda it: str(it).replace('000000000',''), data['time']))
        tempos = pd.to_datetime(devices_time, unit='s')
        return tempos

    def multiple_forecasting_arima(self, data, p, d, q):
        model = ARIMA(data, order=(5,1,0))
        model_fit = model.fit(disp=0)
        # For the default l_bfgs_b solver, disp controls the frequency 
        # of the output during the iterations. disp < 0 means no output in this case.
        # print(model_fit.summary())
        residuals_plots()

        X = series.values
        size = int(len(X) * 0.66)
        train, test = X[0:size], X[size:len(X)]
        history = [x for x in train]
        predictions = list()
        
        # Re-creating the ARIMA model after each new observation is received
        # rolling forecast is required given the dependence on observations 
        # in prior time steps for differencing and the AR model
        for t in range(len(test)):
            model = ARIMA(history, order=(p,d,q))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = test[t]
            history.append(obs)
            print('predicted=%f, expected=%f' % (yhat, obs))

        error = mean_squared_error(test, predictions)
        print('Test MSE: %.3f' % error)
        return error

