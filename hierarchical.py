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
Taxi=pd.read_csv('finaltaxiresid.csv')
del(Taxi['Unnamed: 0'])
Clusters =Taxi.loc[:,{'pickup_lat','pickup_lon','pickup_cluster'}]
Clusters=Clusters.drop_duplicates(subset='pickup_cluster', keep="last")




coords = Clusters.as_matrix(columns=['pickup_lat', 'pickup_lon'])
kms_per_radian = 6371.0088
epsilon = 0.75/ kms_per_radian
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
rep_points = pd.DataFrame({'pickup_lon2':lons, 'pickup_lat2':lats})
rep_points['pickup_cluster2']=np.arange(0,301)
Clusters['pickup_cluster2']=cluster_labels
Clusters = pd.merge(Clusters,rep_points ,on=['pickup_cluster2'], how='left')
Taxi['pickup_cluster2']=Taxi['pickup_cluster']

del(Taxi['pickup_lon'])
del(Taxi['pickup_lat'])
del(Taxi['pickup_cluster2'])

Taxi = pd.merge(Taxi,Clusters ,on=['pickup_cluster'], how='left')



Taxi.to_csv('finalpickuptaxi2.csv')
"""geographic distance from nearest coordinate"""