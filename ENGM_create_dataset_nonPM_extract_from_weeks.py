import pandas as pd
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "ENGM"

months = ['10']

DATA_DIR = os.path.join("data", airport_icao)
WEEKS_DIR = os.path.join(DATA_DIR, "States_50NM")
DATASET_DIR = os.path.join(DATA_DIR, "Dataset")


filename = os.path.join(WEEKS_DIR, "osn_arrival_ENGM_states_50NM_2019_10_week1.csv")
week1_df = pd.read_csv(filename, sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
week1_df.set_index(['flightId', 'sequence'], inplace = True)
num_flights1 = len(week1_df.groupby(level='flightId'))

filename = os.path.join(WEEKS_DIR, "osn_arrival_ENGM_states_50NM_2019_10_week2.csv")
week2_df = pd.read_csv(filename, sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
week2_df.set_index(['flightId', 'sequence'], inplace = True)
num_flights2 = len(week2_df.groupby(level='flightId'))

filename = os.path.join(WEEKS_DIR, "osn_arrival_ENGM_states_50NM_2019_10_week3.csv")
week3_df = pd.read_csv(filename, sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
week3_df.set_index(['flightId', 'sequence'], inplace = True)
num_flights3 = len(week3_df.groupby(level='flightId'))

filename = os.path.join(WEEKS_DIR, "osn_arrival_ENGM_states_50NM_2019_10_week4.csv")
week4_df = pd.read_csv(filename, sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
week4_df.set_index(['flightId', 'sequence'], inplace = True)
num_flights4 = len(week4_df.groupby(level='flightId'))

frames = [week1_df, week2_df, week3_df, week4_df]
month_df = pd.concat(frames)
num_flights = len(month_df.groupby(level='flightId'))


input_filename = "PM.csv"
PM_df = pd.read_csv(os.path.join(DATASET_DIR, input_filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
PM_df.set_index(['flightId', 'sequence'], inplace = True)

output_filename = "nonPM.csv"

flight_ids_list = sorted(list(set(PM_df.index.get_level_values("flightId"))))
#print(len(flight_ids_list))

nonPM_df = pd.DataFrame()

count = 0
number_of_flights = len(month_df.groupby(level='flightId'))

count2 = 0
for flight_id, flight_id_group in month_df.groupby(level='flightId'): 
    count = count + 1
    #print(number_of_flights, count, flight_id)
              
    if flight_id not in flight_ids_list:
        count2 = count2 + 1
        print(number_of_flights, count, count2, flight_id)
        
        nonPM_df = pd.concat([nonPM_df, flight_id_group])

nonPM_df.to_csv(os.path.join(DATASET_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)

print(len(PM_df.groupby(level='flightId')))     # 2145 flights
print(len(nonPM_df.groupby(level='flightId')))  # 5718 flights

