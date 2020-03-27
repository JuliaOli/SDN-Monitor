#influx -database 'database_name' -execute 'SELECT * FROM table_name' -format csv > test.csv

# http://cmdlinetips.com/2018/03/how-to-make-boxplots-in-python-with-pandas-and-seaborn/
# https://www.inf.ufsc.br/~marcelo.menezes.reis/Cap4.pdf
# https://towardsdatascience.com/the-akaike-information-criterion-c20c8fd832f2
# https://www.dnsstuff.com/bandwidth-monitor 
#
# Load the Pandas libraries with alias 'pd' 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from pandas.plotting import autocorrelation_plot
from pandas import DataFrame

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf

from pyramid.arima import auto_arima

from sklearn.metrics import mean_squared_error

class LearningTest:
    def __init__(self, dataAdress):
        self.data = dataAdress
        self.series = pd.read_csv(self.data, delim_whitespace=True)
        self.stewise_model = ''
  
    def timestamp_to_datetime(self, data):
        # https://stackoverflow.com/questions/40023746/plotting-of-pandas-dataframe-and-xaxis-as-timestamp-produces-empty-plot
        # Converts timestamp into datetime format and sets time as the index
        # This function is necessary to plot a correct relation between time and values
        data['time'] = pd.to_datetime(data['time'], unit='s')
        data.set_index('time', inplace=True)


    def autocorrelation_plots(self):
        #plot the valuesXtime
        plt.plot(self.series['value'])

        #autocorrelation plot of the time series
        # Autocorrelation is the correlation of a signal with a delayed 
        # copy — or a lag — of itself as a function of the delay.
        plot_acf(self.series['value'])
        plot_pacf(self.series['value']) # Patial autocorrelation plot
        plt.show()

    def decomposion_plots(self):
        # The decomposition of time series is a statistical task that deconstructs a time series into several components, 
        # each representing one of the underlying categories of patterns. 
        # With statsmodels we will be able to see the trend, seasonal, and residual components of our data.
        #https://stackoverflow.com/questions/34494780/time-series-analysis-unevenly-spaced-measures-pandas-statsmodels
        #w = self.series.index.frequency()
        result = seasonal_decompose(self.series, model='additive', freq=30)
        result.plot()
        plt.show()
    
    def residuals_plots(self, model_fit):
        # Residual of an observed value is the difference between the observed value 
        # and the estimated value of the quantity of interest (for example, a sample mean).
        # After the fitting the model we can obtain our residuals and visualize them
        # Model_fit can be any model class, ex.: ARIMA.
        residuals = DataFrame(model_fit.resid) # Residuals from our model
        residuals.plot()
        # Generate Kernel Density Estimate plot using Gaussian kernels.
        residuals.plot(kind='kde')
        plt.show()
        print(residuals.describe())
    
    def predictions_plots(self, test, predictions):
        # A line plot is created showing the expected values (blue) 
        # compared to the rolling forecast predictions (red). 
        # We can check if the values show some trend and are in the correct scale.
        plt.plot(test)
        plt.plot(predictions, color='red')
        plt.show()

    def aic_score(self, data):
        self.stepwise_model = auto_arima(data, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=12,
                           start_P=0, seasonal=False,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
        print(self.stepwise_model.aic())

    # Define the model by calling ARIMA() and passing in the p, d, and q parameters.
    # The model is prepared on the training data by calling the fit() function.
    # Predictions can be made by calling the predict() function and specifying 
    # the index of the time or times to be predicted.

    def multiple_forecasting_arima(self, data, p, d, q):

        # Re-creating the ARIMA model after each new observation is received
        # rolling forecast is required given the dependence on observations 
        # in prior time steps for differencing and the AR model
        X = data['value']
        size = int(len(X) * 0.66)
        train, test = X[0:size], X[size:len(X)]
        history = [x for x in train]
        predictions = list()
        for t in range(len(test)):
            model = ARIMA(history, order=(5,1,0))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = test[t]
            history.append(obs)
            print('predicted=%f, expected=%f' % (yhat, obs))
        error = mean_squared_error(test, predictions)
        print('Test MSE: %.3f' % error)
        self.predictions_plots(test, predictions)

if __name__ == "__main__":
    learning = LearningTest("/home/julia/Documentos/Laccan/utilization.csv")
    learning.series = learning.series.drop(['device', 'port'], axis=1)
    learning.timestamp_to_datetime(learning.series)
    learning.aic_score(learning.series)
    learning.multiple_forecasting_arima(learning.series, 1, 1, 1)
    
#     while(True):
#         time.sleep(20)
#         monitor.get_stats()
