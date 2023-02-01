import pandas as pd
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "ENGM"

DATA_DIR = os.path.join("data", airport_icao)

DATASET_DIR = os.path.join(DATA_DIR, "Datasets")

ids_filename = "PM_GM418_flights.csv"

ids_df = pd.read_csv(os.path.join(DATASET_DIR, ids_filename), sep=',', index_col=0)

ids_list = list(ids_df["flightId"])
print(ids_list)

input_nonPM_filename = "nonPM3.csv"
input_PM_filename = "PM.csv"

output_nonPM_filename = "nonPM_final.csv"
output_PM_filename = "PM_final.csv"


nonPM_df = pd.read_csv(os.path.join(DATASET_DIR, input_nonPM_filename), sep=' ',
            names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])

nonPM_df.set_index(['flightId', 'sequence'], inplace=True)


PM_df = pd.read_csv(os.path.join(DATASET_DIR, input_PM_filename), sep=' ',
            names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])

PM_df.set_index(['flightId', 'sequence'], inplace=True)


list_length = len(ids_list)
count = 0


for flight_id in ids_list:
    count = count + 1
    print(list_length, count)
    try:
        flight_df = nonPM_df.loc[[flight_id]]
        PM_df = pd.concat([PM_df, flight_df])
        nonPM_df = nonPM_df.drop(flight_id)
    except:
        print(flight_id + ' not in nonPM dataset')
        
PM_df = PM_df.sort_index(level=['flightId', 'sequence'])
          
nonPM_df.to_csv(os.path.join(DATASET_DIR, output_nonPM_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
PM_df.to_csv(os.path.join(DATASET_DIR, output_PM_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
