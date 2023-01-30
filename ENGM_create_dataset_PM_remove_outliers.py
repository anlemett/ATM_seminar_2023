import numpy as np
import pandas as pd

import os

import time
start_time = time.time()

year = '2019'
airport_icao = "ENGM"


DATA_DIR = os.path.join("data", airport_icao)
DATASET_DATA_DIR = os.path.join(DATA_DIR, "Dataset")

states_df = pd.DataFrame()

filename = "PM1.csv"
states_df = pd.read_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

num_flights = len(states_df.groupby(level='flightId'))
print(num_flights)

flight_ids_list = ["191007WIF96B", "191018NAX9KP", "191009SAS2306", "191016SAS65P"]


list_length = len(flight_ids_list)
count = 0

for flight_id in flight_ids_list:
    count = count + 1
    print(list_length, count)
    try:
        states_df = states_df.drop(flight_id)
    except:
        print(flight_id + ' not in dataset')
    
filename = "PM.csv"
states_df.to_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)