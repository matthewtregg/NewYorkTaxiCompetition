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
os.chdir(r'C:\Users\usuario\Downloads')
Taxi=pd.read_csv('dropofftaxi5.csv')

del(Taxi['Unnamed: 0'])


Taxi1=Taxi.loc[((Taxi['dropoff_cluster']==1328)),:]
Taxi2=Taxi.loc[~(Taxi['dropoff_cluster']==1328),:]
Taxi1['dropoff_cluster6']=Taxi1['dropoff_cluster']

del(Taxi1['dropoff_lat'])
del(Taxi1['dropoff_lon'])
del(Taxi1['dropoff_cluster'])



coords = Taxi1.as_matrix(columns=['dropoff_latitude', 'dropoff_longitude'])
kms_per_radian = 6371.0088
epsilon = 0.1/ kms_per_radian
db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
cluster_labels = db.labels_
num_clusters = len(set(cluster_labels))
clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
print('Number of clusters: {}'.format(num_clusters))

def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)
centermost_points = clusters.map(get_centermost_point)
lats, lons = zip(*centermost_points)
rep_points = pd.DataFrame({'dropoff_lon':lons, 'dropoff_lat':lats})
rep_points['dropoff_cluster']=np.arange(0,117)
Taxi1['dropoff_cluster']=cluster_labels
Taxi1 = pd.merge(Taxi1,rep_points ,on=['dropoff_cluster'], how='left')

Taxi1['dropoff_cluster']=Taxi1['dropoff_cluster']+445+531+210+142+137

"""Taxi['route_index']= list(zip(Taxi['dropoff_cluster'],Taxi['pickup_cluster']))"""
Taxi1.to_csv('dropofftaxi6.csv')
Taxi2.to_csv('Not_dropofftaxi6.csv')
