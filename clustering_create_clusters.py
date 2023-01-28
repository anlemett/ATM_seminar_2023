import numpy as np
import pandas as pd
from shapely.geometry import Point
import os
from sklearn.cluster import KMeans
import math

import time
start_time = time.time()

year = '2019'
airport_icao = "ENGM"

number_of_clusters = 6


DATA_DIR = os.path.join("data", airport_icao)
DATASET_DATA_DIR = os.path.join(DATA_DIR, "Dataset")
DATA_DIR = os.path.join(DATA_DIR, "Clustering")


#input_dataset = "PM_SOUTH"
input_dataset = "PM_NORTH"
input_filename = input_dataset + "_borders_points.csv"
input_states_filename = input_dataset + ".csv"
output_filename = input_dataset + "_clusters_" + str(number_of_clusters) + ".csv"


points_df = pd.read_csv(os.path.join(DATA_DIR, input_filename), sep=' ')
points_df.set_index(['flight_id'], inplace=True)

number_of_flights = len(points_df.groupby(level='flight_id'))
print(number_of_flights)

points = np.zeros(shape=(number_of_flights, 2))

i = 0
for flight_id, row in points_df.iterrows():
    
    points[i] = [row['lon'], row['lat']]
    i = i + 1
    
# create kmeans object
kmeans = KMeans(n_clusters=number_of_clusters)

# fit kmeans object to data
kmeans.fit(points)

# save new clusters
clusters = kmeans.fit_predict(points)

points_df['cluster'] = clusters

def getClusterLon(cluster):
    return kmeans.cluster_centers_[int(cluster), 0]

def getClusterLat(cluster):
    return kmeans.cluster_centers_[int(cluster), 1]

points_df['center_lat'] = points_df.apply(lambda row: getClusterLat(row['cluster']), axis=1)
points_df['center_lon'] = points_df.apply(lambda row: getClusterLon(row['cluster']), axis=1)


# Renumerate clusters
lon_lat_cluster_list = []

for cluster in range(0, number_of_clusters):
    
    lon_lat_cluster_list.append([points_df[points_df['cluster']==cluster]['center_lon'].to_list()[0],
                                 points_df[points_df['cluster']==cluster]['center_lat'].to_list()[0],
                                 cluster])

highest = max(lon_lat_cluster_list, key = lambda x: (x[1], x[0]))

sorted_points = sorted(lon_lat_cluster_list, key=lambda x: math.atan2(highest[1]-x[1], highest[0]-x[0]) + 2 * math.pi, reverse=True)

sorted_cluster_numbers = [item[2] for item in sorted_points]


def renumerateClusters(old_cluster_number):
    return sorted_cluster_numbers.index(old_cluster_number)

points_df['cluster'] = points_df.apply(lambda row: renumerateClusters(row['cluster']), axis=1)


def fixClusterNumber(cluster):
    return int(cluster + 1)

points_df['cluster'] = points_df.apply(lambda row: fixClusterNumber(row['cluster']), axis=1)


points_df.to_csv(os.path.join(DATA_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = True)   





# Creating cluster states files
'''
clusters_df_list = []
for i in range(0, number_of_clusters):
    df = pd.DataFrame()
    clusters_df_list.append(df)

states_df = pd.read_csv(os.path.join(DATASET_DATA_DIR, input_states_filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
states_df.set_index(['flightId', 'sequence'], inplace = True)

count = 0
number_of_flights = len(states_df.groupby(level='flightId')) 

for flight_id, row in points_df.iterrows():
    
    count = count + 1
    print(number_of_flights, count, flight_id)
    
    row_cluster = int(row['cluster']) - 1
    #print(row_cluster)

    flight_df = states_df[states_df.index.get_level_values('flightId') == flight_id]
    if flight_df.empty:
        continue
    clusters_df_list[row_cluster] = clusters_df_list[row_cluster].append(flight_df)
    
CLUSTERS_DATA_DIR = os.path.join(DATASET_DATA_DIR, input_dataset + "_clusters")
if not os.path.exists(CLUSTERS_DATA_DIR):
    os.makedirs(CLUSTERS_DATA_DIR)
    
for i in range(0, number_of_clusters):
    output_states_filename = input_states_filename + "_cluster" + str(i+1) + ".csv"
    clusters_df_list[i].to_csv(os.path.join(CLUSTERS_DATA_DIR, output_states_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
  ''' 