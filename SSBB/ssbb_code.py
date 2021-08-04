# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 11:46:29 2021

@author: window 10
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

pd.options.display.max_rows=110
pd.options.display.max_columns=6
data = pd.read_excel('Cleaned_SSBB.xlsx')
data.shape
data.columns
data.head()

data['Counsellor_name'].value_counts()
data.groupby('Counsellor_name').sum()

data['Course_type'].value_counts()

data['Fees_pending'].value_counts()

data = data.drop(["Fees_pending"] , axis = 1)
data
data.rename(columns= {'time' : "Date"} , inplace = True )
data.columns
data.isnull().sum()

data.info()

data.describe()
data.shape
data['year'] = pd.DatetimeIndex(data['Date']).year
data['month'] = pd.DatetimeIndex(data['Date']).month

data.head()

data.to_excel("m_SSBB.xlsx")



import seaborn as sns

plt.rcParams['figure.figsize']=(17,5)
sns.boxplot(data['Fees_received'], color='green')

data['Fees_Total'].loc[(data['Fees_Total']>=90525)] = 90525
data['Fees_Total'].loc[(data['Fees_Total']<=3500)] = 3500
plt.rcParams['figure.figsize']=(17,5)
sns.boxplot(data['Fees_Total'], color='green')


import statsmodels.api as sm
##2020
List = []
for x in range(4, 13):
    List.append(data.loc[(data['year'] == 2020) & (data['month'] == x), 'Fees_Total'].sum())
 print(List)

#2021
for x in range(1, 8):
    List.append(data.loc[(data['year'] == 2021) & (data['month'] == x), 'Fees_Total'].sum())
print(List)  


List2=['1/4/20','1/5/20','1/6/20','1/7/20','1/8/20','1/9/20','1/10/20','1/11/20','1/12/20','1/1/21','1/2/21','1/3/21','1/4/21','1/5/21','1/6/21','1/7/21']


from datetime import datetime
for i in List2:
    i=datetime.strptime(i, '%d/%m/%y')
    
List2    
df = pd.DataFrame(list(zip(List2, List)),
               columns =['Dates', 'Revenue'])
df

index= pd.date_range(start='2020-04-01', end='2021-07-01', freq='MS')
revenue = pd.Series(List, index)
revenue

plt.figure(figsize =[12,10])
plt.plot(revenue,label = "index"  )
plt.legend(loc = "upper left")
plt.grid(True)

from statsmodels.tsa.api import ExponentialSmoothing
fit1 = ExponentialSmoothing(revenue, seasonal_periods=5, trend='multiplicative', seasonal='additive').fit(smoothing_level=0.94,smoothing_trend=0.01)
fit1.fittedvalues

# Forecast for 12 years
fore_cast = fit1.forecast(12)
fore_cast

#plotting Revenue and forecasted sales
plt.figure(figsize=[12,10])
plt.grid(True)
plt.plot(revenue,label='past data')
plt.plot(fore_cast,label='forecast')
x_values = [revenue.index[-1], fore_cast.index[0]]
y_values = [revenue[-1], fore_cast[0]]
plt.plot(x_values, y_values)
plt.legend(loc = "upper left")

# code for Counsellor_wise sales and their forcasted for 12 months period
data['Counsellor_name'].value_counts()
#tarun
data1 = data[data['Counsellor_name'] == 'Tarun']
data1

A = []
for x in range(4, 13):
    A.append(data1.loc[(data['year'] == 2020) & (data['month'] == x), 'Fees_Total'].sum())
print(A)
 
for x in range(1, 8):
    A.append(data1.loc[(data['year'] == 2021) & (data['month'] == x), 'Fees_Total'].sum())
print(A)

index= pd.date_range(start='2020-04-01', end='2021-07-01', freq='MS')
revenueByTarun = pd.Series(A, index)
revenueByTarun

from statsmodels.tsa.api import ExponentialSmoothing
fit3 = ExponentialSmoothing(revenueByTarun, seasonal_periods=5, trend='additive', seasonal='additive').fit(smoothing_level=0.94,smoothing_trend=0.01)    
fit3.fittedvalues
fcast3 = fit3.forecast(12)
fcast3
plt.figure(figsize=[15,8])
plt.grid(True)
plt.plot(revenueByTarun,label='past data')
plt.plot(fcast2,label='forecast')
x_values = [revenueByTarun.index[-1], fcast2.index[0]]
y_values = [revenueByTarun[-1], fcast2[0]]
plt.plot(x_values, y_values)
plt.legend(loc=2)

# similar code for Course-wise sales and forcasted revenue