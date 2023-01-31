import numpy as np
import pandas as pd
from shapely.geometry import Point
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "ENGM"

DATA_DIR = os.path.join("data", airport_icao)

DATASET_DIR = os.path.join(DATA_DIR, "Datasets")

input_filename = "PM.csv"

output_filename1 = "PM_SOUTH.csv"
output_filename2 = "PM_NORTH.csv"


states_df = pd.read_csv(os.path.join(DATASET_DIR, input_filename), sep=' ',
            names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])


states_df.set_index(['flightId', 'sequence'], inplace=True)

filename = os.path.join(DATA_DIR, "runways_2019_10_week1.csv")
rwys_week1_df = pd.read_csv(filename, sep=' ', dtype = {'date': str})

filename = os.path.join(DATA_DIR, "runways_2019_10_week2.csv")
rwys_week2_df = pd.read_csv(filename, sep=' ', dtype = {'date': str})

filename = os.path.join(DATA_DIR, "runways_2019_10_week3.csv")
rwys_week3_df = pd.read_csv(filename, sep=' ', dtype = {'date': str})

filename = os.path.join(DATA_DIR, "runways_2019_10_week4.csv")
rwys_week4_df = pd.read_csv(filename, sep=' ', dtype = {'date': str})

rwys_df = pd.concat([rwys_week1_df, rwys_week2_df, rwys_week3_df, rwys_week4_df])

rwys_df.set_index(['flight_id'], inplace=True)


PM_south_df = pd.DataFrame()
PM_north_df = pd.DataFrame()

count = 0
number_of_flights = len(states_df.groupby(level='flightId'))

for flight_id, flight_id_group in states_df.groupby(level='flightId'): 
    count = count + 1
    print(number_of_flights, count, flight_id)
    
    rwy = rwys_df.loc[flight_id]['runway']

    if (rwy == '01R') or (rwy == '01L'):
        
        PM_south_df = pd.concat([PM_south_df, flight_id_group])
        
    else:
        
        PM_north_df = pd.concat([PM_north_df, flight_id_group])



PM_south_df.to_csv(os.path.join(DATASET_DIR, output_filename1), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)

PM_north_df.to_csv(os.path.join(DATASET_DIR, output_filename2), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)

