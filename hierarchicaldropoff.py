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
Taxi=pd.read_csv('dropofffinaltaxiresid.csv')
del(Taxi['Unnamed: 0'])
del(Taxi['Unnamed: 0.1'])



Taxi['dropoff_clusterFINAL']=Taxi['dropoff_cluster']


del(Taxi['dropoff_cluster'])



coords = Taxi.as_matrix(columns=['dropoff_lat', 'dropoff_lon'])
kms_per_radian = 6371.0088
epsilon = 0.3/ kms_per_radian
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
rep_points = pd.DataFrame({'dropoff_lon2':lons, 'dropoff_lat2':lats})
rep_points['dropoff_cluster']=np.arange(0,1351)
Taxi['dropoff_cluster']=cluster_labels
Taxi = pd.merge(Taxi,rep_points ,on=['dropoff_cluster'], how='left')

Taxi['dropoff_cluster']=Taxi['dropoff_cluster']


Taxi.to_csv('finaldropofftaxi.csv')
"""geographic distance from nearest coordinate"""
