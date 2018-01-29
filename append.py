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
from geopy.distance import vincenty
from shapely.geometry import MultiPoint
os.chdir(r'C:\Users\usuario\Downloads')

Taxi4=pd.read_csv('fulltaxi3.csv')
Taxi3=pd.read_csv('Not_fulltaxi3.csv')
Taxi2=pd.read_csv('Not_fulltaxi2.csv')
Taxi1=pd.read_csv('Not_fulltaxi1.csv')
del(Taxi1['Unnamed: 0'])
del(Taxi1['Unnamed: 0.1'])

del(Taxi2['Unnamed: 0'])
del(Taxi2['Unnamed: 0.1'])
del(Taxi2['Unnamed: 0.1.1'])

del(Taxi3['Unnamed: 0'])
del(Taxi3['Unnamed: 0.1'])
del(Taxi3['Unnamed: 0.1.1'])


del(Taxi4['Unnamed: 0'])
del(Taxi4['Unnamed: 0.1'])
del(Taxi4['Unnamed: 0.1.1'])


Taxi=pd.read_csv('fulltaxi.csv')
del(Taxi['Unnamed: 0'])

Final_Taxi=Taxi1.append(Taxi2)
Final_Taxi=Final_Taxi.append(Taxi3)
Final_Taxi=Final_Taxi.append(Taxi4)


def distance_calc(row):
    start = (row['pickup_latitude'], row['pickup_longitude'])
    stop = (row['pickup_lat'], row['pickup_lon'])
    return vincenty(start, stop).meters

Final_Taxi['pickup_resid'] = Final_Taxi.apply (lambda row: distance_calc (row),axis=1)





Final_Taxi.to_csv('finaltaxiresid.csv')