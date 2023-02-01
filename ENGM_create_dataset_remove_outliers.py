import pandas as pd

import os

import time
start_time = time.time()

year = '2019'
airport_icao = "ENGM"


DATA_DIR = os.path.join("data", airport_icao)
DATASET_DATA_DIR = os.path.join(DATA_DIR, "Datasets")

states_df = pd.DataFrame()

#filename = "TT1.csv"
filename = "nonPM.csv"
states_df = pd.read_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

num_flights = len(states_df.groupby(level='flightId'))
print(num_flights)

#filename = "TT_error_flights.txt"
filename = "nonPM_error_flights.txt"

flight_ids_list = open(os.path.join(DATASET_DATA_DIR, filename),'r').read().split('\n')
flight_ids_list = flight_ids_list[:-1]

list_length = len(flight_ids_list)
count = 0

for flight_id in flight_ids_list:
    count = count + 1
    print(list_length, count)
    try:
        states_df = states_df.drop(flight_id)
    except:
        print(flight_id + ' not in dataset')
    
filename = "nonPM3.csv"
states_df.to_csv(os.path.join(DATASET_DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)