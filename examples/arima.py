# https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/
#
#  A popular and widely used statistical 
# method for time series forecasting is the ARIMA model.
# 
# ARIMA is an acronym that stands for AutoRegressive Integrated Moving Average.
# It is a class of model that captures a suite of different 
# standard temporal structures in time series data.

#This acronym is descriptive, capturing the key aspects of the model itself. Briefly, they are:
# AR: Autoregression. A model that uses the dependent relationship between an observation and some number of lagged observations.
# I: Integrated. The use of differencing of raw observations (e.g. subtracting an observation from an observation at the previous time step) in order to make the time series stationary.
# MA: Moving Average. A model that uses the dependency between an observation and a residual error from a moving average model applied to lagged observations.

# Each of the components are explicitly specified in the model as a parameter.
# A standard notation is used of ARIMA(p,d,q) where the parameters are substituted 
# with integer values to quickly indicate the specific ARIMA model being used.

# The parameters of the ARIMA model are defined as follows:

#     p: The number of lag observations included in the model, also called the lag order. 
# 		 (The lag length is how many terms back down the AR process you want to test for serial correlation)
#     d: The number of times that the raw observations are differenced, also called the degree of differencing.
#     q: The size of the moving average window, also called the order of moving average.

#A value of 0 can be used for a parameter, which indicates to not use that element of the model. 

from pandas import read_csv
from pandas import datetime
from pandas.plotting import autocorrelation_plot
from pandas import DataFrame

from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from sklearn.metrics import mean_squared_error

# loading the Shampoo Sales dataset with Pandas
# with a custom function to parse the date-time field

def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')
 
series = read_csv("/home/mj/Documentos/Git Lab repositories/Version_control_backup/Git/SDN-Monitor/examples/db/shampoo_sales_example.csv", header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
print(series.head())
series.plot()

# the time series is not stationary 
# and will require differencing to make it stationary, at least a difference order of 1.
# Stationary time series is when the mean and variance are constant over time. 
# It is easier to predict when the series is stationary.

#plots the autocorrelation for a large number of lags in the time series.
# ACF plot
plot_acf(series)
plot_pacf(series)
#autocorrelation_plot(series) #esse aqui é mais completo
pyplot.show()

# An ARIMA model can be created using the statsmodels library as follows:

#   Define the model by calling ARIMA() and passing in the p, d, and q parameters.
#   The model is prepared on the training data by calling the fit() function.
#   Predictions can be made by calling the predict() function and specifying the index of the time or times to be predicted.

# Fit an ARIMA(5,1,0) model. 
# This sets the lag value to 5 for autoregression,
# uses a difference order of 1 to make the time series stationary, 
# and uses a moving average model of 0.

# fit model
model = ARIMA(series, order=(5,1,0))
model_fit = model.fit(disp=0) #If True, convergence information is printed.
# For the default l_bfgs_b solver, disp controls the frequency of the output during the iterations. disp < 0 means no output in this case.
print(model_fit.summary())

# plot residual errors
residuals = DataFrame(model_fit.resid)
residuals.plot()
pyplot.show()
residuals.plot(kind='kde')
pyplot.show()
print(residuals.describe())

# Summarizes the coefficient values used as well as the skill of the fit
# on the on the in-sample observations.

# First, we get a line plot of the residual errors, suggesting that there may 
# still be some trend information not captured by the model.

# Next, we get a density plot of the residual error values, 
# suggesting the errors are Gaussian, but may not be centered on zero.

# The distribution of the residual errors is displayed. 
# The results show that indeed there is a bias in the prediction (a non-zero mean in the residuals).

#Rolling forecast: predictions and residuals

X = series.values
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

# plot
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()
