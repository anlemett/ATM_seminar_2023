import pandas as pd
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "ENGM"

DATA_DIR = os.path.join("data", airport_icao)

DATASET_DIR = os.path.join(DATA_DIR, "Datasets")

#dataset = "TT"
#dataset = "PM"
dataset = "nonPM2"

input_filename = dataset + ".csv"

output_filename_north = dataset + "_NORTH.csv"
output_filename_south = dataset + "_SOUTH.csv"


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


south_df = pd.DataFrame()
north_df = pd.DataFrame()

count = 0
number_of_flights = len(states_df.groupby(level='flightId'))

for flight_id, flight_id_group in states_df.groupby(level='flightId'): 
    count = count + 1
    print(number_of_flights, count, flight_id)
    
    rwy = rwys_df.loc[flight_id]['runway']

    if (rwy == '01R') or (rwy == '01L'):
        
        south_df = pd.concat([south_df, flight_id_group])
        
    else:
        
        north_df = pd.concat([north_df, flight_id_group])

north_df.to_csv(os.path.join(DATASET_DIR, output_filename_north), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)

south_df.to_csv(os.path.join(DATASET_DIR, output_filename_south), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
