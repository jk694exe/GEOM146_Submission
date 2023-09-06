# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 22:15:15 2023

@author: Jasleen
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


dataset = pd.read_csv("windVfOutput.csv")
X = dataset.iloc[:,:5].values #import all columns except the last one
y = dataset.iloc[:,-1].values #import the last column
y = y.reshape(y.size,1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

regressor = LinearRegression(fit_intercept=True)
regressor.fit(X_train, y_train)

y_pred_train = regressor.predict(X_train)
y_pred_test = regressor.predict(X_test)

SSres_train = np.sum(np.power(y_train - y_pred_train,2),axis=0)
yavg_train = np.sum(y_train, axis=0)/y_train.size
SStot_train = np.sum(np.power(y_train - yavg_train,2),axis=0)
rsq_train = 1 - (SSres_train/SStot_train)

SSres_test = np.sum(np.power(y_test - y_pred_test,2),axis=0)
yavg_test = np.sum(y_test, axis=0)/y_test.size
SStot_test = np.sum(np.power(y_test - yavg_test,2),axis=0)
rsq_test = 1 - (SSres_test/SStot_test)


print("Coefficients")
print (regressor.coef_)
print(regressor.intercept_)
print("R squared values: Training Set: " + str(rsq_train) + " Test Set: " + str(rsq_test))

import statsmodels.api as sma

X2  = sma.add_constant(X_train)
est  = sma.OLS(y_train, X2)
est_2  = est.fit()
print(est_2.summary())