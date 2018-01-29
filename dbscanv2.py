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
Taxi=pd.read_csv('fulltaxi.csv')
Taxi1=Taxi.loc[((Taxi['pickup_cluster']==1)|(Taxi['pickup_cluster']==0)|(Taxi['pickup_cluster']==3)),:]
Taxi2=Taxi.loc[~((Taxi['pickup_cluster']==1)|(Taxi['pickup_cluster']==0)|(Taxi['pickup_cluster']==3)),:]

Taxi1['pickup_cluster2']=Taxi1['pickup_cluster']
del(Taxi1['pickup_cluster'])
del(Taxi1['pickup_lon'])
del(Taxi1['pickup_lat'])


"""Taxi index values """
coords = Taxi1.as_matrix(columns=['pickup_latitude', 'pickup_longitude'])
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
rep_points = pd.DataFrame({'pickup_lon':lons, 'pickup_lat':lats})
rep_points['pickup_cluster']=np.arange(0,174)
Taxi1['pickup_cluster']=cluster_labels
Taxi1 = pd.merge(Taxi1,rep_points ,on=['pickup_cluster'], how='left')

Taxi1['pickup_cluster']=Taxi1['pickup_cluster']+315





Taxi1.to_csv('fulltaxi1.csv')
Taxi2.to_csv('Not_fulltaxi1.csv')
"""geographic distance from nearest coordinate"""

