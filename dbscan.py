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
Taxi=pd.read_csv('final_taxi.csv')

#
Taxi=Taxi.iloc[:,6::]
del(Taxi['ehail_fee'])
del(Taxi['extra'])
del(Taxi['trip_type'])
del(Taxi['tip_amount'])
del(Taxi['tolls_amount'])
del(Taxi['store_and_fwd_flag'])
del(Taxi['payment_type'])
del(Taxi['improvement_surcharge'])
del(Taxi['mta_tax'])





"""Taxi index values """
coords = Taxi.as_matrix(columns=['pickup_latitude', 'pickup_longitude'])
kms_per_radian = 6371.0088
epsilon = 0.5/ kms_per_radian
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
rep_points = pd.DataFrame({'pickup_lon':lons, 'pickup_lat':lats})
rep_points['pickup_cluster']=np.arange(0,315)
Taxi['pickup_cluster']=cluster_labels
Taxi = pd.merge(Taxi,rep_points ,on=['pickup_cluster'], how='left')







coords = Taxi.as_matrix(columns=['dropoff_latitude', 'dropoff_longitude'])
kms_per_radian = 6371.0088
epsilon = 0.5/ kms_per_radian
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
rep_points['dropoff_cluster']=np.arange(0,1059)
Taxi['dropoff_cluster']=cluster_labels
Taxi = pd.merge(Taxi,rep_points ,on=['dropoff_cluster'], how='left')

"""Taxi['route_index']= list(zip(Taxi['dropoff_cluster'],Taxi['pickup_cluster']))"""
Taxi.to_csv('fulltaxi.csv')

"""geographic distance from nearest coordinate"""

