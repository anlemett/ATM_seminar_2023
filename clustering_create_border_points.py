import numpy as np
import pandas as pd
from shapely.geometry import Point
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "ENGM"

DATA_DIR = os.path.join("data", airport_icao)

DATA_INPUT_DIR = os.path.join(DATA_DIR, "Dataset")

DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "Clustering")


input_filename = "PM_south"

output_filename = input_filename + "_borders_points.csv"


states_df = pd.read_csv(os.path.join(DATA_INPUT_DIR, input_filename + ".csv"), sep=',',
                    index_col=0)

states_df.set_index(['flightID', 'sequence'], inplace=True)
    
borders_points_df = pd.DataFrame(columns=['flight_id', 'lat', 'lon'])

count = 0
number_of_flights = len(states_df.groupby(level='flightID'))  

for flight_id, flight_df in states_df.groupby(level='flightID'): 
    count = count + 1
    print(number_of_flights, count, flight_id)
    
    entry_point_lon = flight_df['lon'][0]
    entry_point_lat = flight_df['lat'][0]
    
    borders_points_df = pd.concat([borders_points_df, pd.DataFrame({'flight_id': [flight_id],
                            'lat': [entry_point_lat], 
                            'lon': [entry_point_lon]})])
        
borders_points_df.to_csv(os.path.join(DATA_OUTPUT_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)   
        
        
input_filename = "PM_north"

output_filename = input_filename + "_borders_points.csv"


states_df = pd.read_csv(os.path.join(DATA_INPUT_DIR, input_filename + ".csv"), sep=',',
                    index_col=0)

states_df.set_index(['flightID', 'sequence'], inplace=True)
    
borders_points_df = pd.DataFrame(columns=['flight_id', 'lat', 'lon'])

count = 0
number_of_flights = len(states_df.groupby(level='flightID'))  

for flight_id, flight_df in states_df.groupby(level='flightID'): 
    count = count + 1
    print(number_of_flights, count, flight_id)
    
    entry_point_lon = flight_df['lon'][0]
    entry_point_lat = flight_df['lat'][0]
    
    borders_points_df = pd.concat([borders_points_df, pd.DataFrame({'flight_id': [flight_id],
                            'lat': [entry_point_lat], 
                            'lon': [entry_point_lon]})])
        
borders_points_df.to_csv(os.path.join(DATA_OUTPUT_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)   
        
        