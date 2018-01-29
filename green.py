# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import os
from datetime import datetime
os.chdir(r'C:\Users\usuario\Downloads')
green=pd.read_csv('green_tripdata_2015-07.csv')


green_columns= green.columns.tolist()
green_columns[1]= 'tpep_dropoff_datetime'
green_columns[2]= 'tpep_pickup_datetime'
old_columns= green.columns
green.rename(columns=dict(zip(old_columns, green_columns)),inplace=True)

green['tpep_dropoff_datetime']= pd.to_datetime(green['tpep_dropoff_datetime'])
X = datetime.datetime.strptime("20/07/15 00:00", "%d/%m/%y %H:%M")
Y = datetime.datetime.strptime("27/07/15 00:00", "%d/%m/%y %H:%M")
green = green.loc[green['tpep_dropoff_datetime']<Y,:] 
green = green.loc[green['tpep_dropoff_datetime']>X,:] 

green.to_csv('green.csv')