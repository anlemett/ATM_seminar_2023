import pandas as pd
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "ENGM"

months = ['10']

DATA_DIR = os.path.join("data", airport_icao)
STATES_DIR = os.path.join(DATA_DIR, "States_50NM")
DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "Dataset")


filename = os.path.join(STATES_DIR, "osn_arrival_ENGM_states_50NM_2019_10_week1.csv")
week1_df = pd.read_csv(filename, sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
week1_df.set_index(['flightId', 'sequence'], inplace = True)
num_flights1 = len(week1_df.groupby(level='flightId'))

filename = os.path.join(STATES_DIR, "osn_arrival_ENGM_states_50NM_2019_10_week2.csv")
week2_df = pd.read_csv(filename, sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
week2_df.set_index(['flightId', 'sequence'], inplace = True)
num_flights2 = len(week2_df.groupby(level='flightId'))

filename = os.path.join(STATES_DIR, "osn_arrival_ENGM_states_50NM_2019_10_week3.csv")
week3_df = pd.read_csv(filename, sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
week3_df.set_index(['flightId', 'sequence'], inplace = True)
num_flights3 = len(week3_df.groupby(level='flightId'))

filename = os.path.join(STATES_DIR, "osn_arrival_ENGM_states_50NM_2019_10_week4.csv")
week4_df = pd.read_csv(filename, sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
week4_df.set_index(['flightId', 'sequence'], inplace = True)
num_flights4 = len(week4_df.groupby(level='flightId'))



frames = [week1_df, week2_df, week3_df, week4_df]
month_df = pd.concat(frames)
num_flights = len(month_df.groupby(level='flightId'))


PIs_DIR = os.path.join(DATA_DIR, "PIs")

filename = os.path.join(PIs_DIR, "PIs_50NM_time_by_flight_2019_10_week1.csv")
pi_by_flight_week1_df = pd.read_csv(filename, sep=' ')

filename = os.path.join(PIs_DIR, "PIs_50NM_time_by_flight_2019_10_week2.csv")
pi_by_flight_week2_df = pd.read_csv(filename, sep=' ')

filename = os.path.join(PIs_DIR, "PIs_50NM_time_by_flight_2019_10_week3.csv")
pi_by_flight_week3_df = pd.read_csv(filename, sep=' ')

filename = os.path.join(PIs_DIR, "PIs_50NM_time_by_flight_2019_10_week4.csv")
pi_by_flight_week4_df = pd.read_csv(filename, sep=' ')

frames = [pi_by_flight_week1_df, pi_by_flight_week2_df, pi_by_flight_week3_df, pi_by_flight_week4_df]
pi_by_flight_df = pd.concat(frames)
# flight_id begin_date end_date begin_hour end_hour 50NM_time_sec 50NM_time_min


filename = os.path.join(PIs_DIR, "PIs_50NM_time_by_hour_2019_10_week1.csv")
pi_by_hour_week1_df = pd.read_csv(filename, sep=' ')

filename = os.path.join(PIs_DIR, "PIs_50NM_time_by_hour_2019_10_week2.csv")
pi_by_hour_week2_df = pd.read_csv(filename, sep=' ')

filename = os.path.join(PIs_DIR, "PIs_50NM_time_by_hour_2019_10_week3.csv")
pi_by_hour_week3_df = pd.read_csv(filename, sep=' ')

filename = os.path.join(PIs_DIR, "PIs_50NM_time_by_hour_2019_10_week4.csv")
pi_by_hour_week4_df = pd.read_csv(filename, sep=' ')

frames = [pi_by_hour_week1_df, pi_by_hour_week2_df, pi_by_hour_week3_df, pi_by_hour_week4_df]
pi_by_hour_df = pd.concat(frames)

#date hour number_of_flights_by_end number_of_flights_by_start_and_end 50NM_time_mean_sec 50NM_time_mean_min

# drop 0.7 percentile

df = pi_by_hour_df

df = df[df['numberOfFlightsByStartAnd_End']>0]
p1 = df["totalTimeMeanMin"].quantile(0.7) #  13.02 min, 3156 flights out of 7863 flights


df = df.loc[(df['totalTimeMeanMin'] > p1)]

print(len(df))

# extract the flights for given hours

df = df.rename(columns = {'date': 'endDate', 'hour': 'endHour'}, inplace = False)

print(df.head(1))


df_inner = pd.merge(df, pi_by_flight_df, on=['endDate', 'endHour'], how='inner')
df_inner = df_inner[['flightId']]

flight_ids_list = df_inner['flightId'].to_list()

#print(num_flights)
#print(p1)
#print(len(df_inner))
#print(len(flight_ids_list))
#print(flight_ids_list)
#exit(0)

dataset_df = pd.DataFrame()
count = 0
number_of_flights = len(month_df.groupby(level='flightId'))

count2 = 0
for flight_id, flight_id_group in month_df.groupby(level='flightId'): 
    count = count + 1
    #print(number_of_flights, count, flight_id)
              
    if flight_id in flight_ids_list:
        count2 = count2 + 1
        print(number_of_flights, count, count2, flight_id)
        
        dataset_df = pd.concat([dataset_df, flight_id_group])

    
filename = "TT1.csv"
dataset_df.to_csv(os.path.join(DATA_OUTPUT_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)

month_number_of_flights = len(month_df.groupby(level='flightId'))
dataset_number_of_flights = len(dataset_df.groupby(level='flightId'))


print(p1)
print(month_number_of_flights)
print(dataset_number_of_flights)