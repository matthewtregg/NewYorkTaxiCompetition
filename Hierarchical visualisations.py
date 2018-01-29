# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 19:14:57 2017

@author: usuario
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint
from geopy.distance import vincenty

os.chdir(r'C:\Users\usuario\Downloads')
Taxi=pd.read_csv('finalpickuptaxi2.csv')


def distance_calc(row):
    start = (row['pickup_latitude'], row['pickup_longitude'])
    stop = (row['pickup_lat2'], row['pickup_lon2'])
    return vincenty(start, stop).meters

Taxi['finalpickup_resid'] = Taxi.apply (lambda row: distance_calc (row),axis=1)

Taxi['green_count'] = np.where(Taxi['taxi_type']=='green', 1,0)
Taxi['index']=np.arange(0,50203)

Taxi.to_csv('FINAL_PICKUP_TAXIS.csv')

