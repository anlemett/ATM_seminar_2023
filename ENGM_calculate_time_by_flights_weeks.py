import pandas as pd
from datetime import datetime
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "ENGM"

months = ['10']

DATA_DIR = os.path.join("data", airport_icao)
STATES_DIR = os.path.join(DATA_DIR, "States_50NM")
DATA_OUTPUT_DIR = os.path.join(DATA_DIR, "PIs")


def get_all_states(csv_input_file):

    df = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':int, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
    
    df = df[['flightId', 'sequence', 'timestamp', 'altitude', 'velocity', 'beginDate', 'endDate']]
    
    df.set_index(['flightId', 'sequence'], inplace=True)
    
    return df


def calculate_50NM_time_by_flight(month, week):
    
    input_filename = "osn_arrival_"+ airport_icao + "_states_50NM_" + year + '_' + str(month) + "_week" + str(week) + ".csv"
    full_input_filename = os.path.join(STATES_DIR, input_filename)
         
    output_filename = "PIs_50NM_time_by_flight_" + year + '_' +  str(month) + "_week" + str(week)+ ".csv"
    full_output_filename = os.path.join(DATA_OUTPUT_DIR, output_filename)
     
    
    states_df = get_all_states(full_input_filename)
   
    pi_df = pd.DataFrame(columns=['flightId', 'beginDate', 'endDate',
                                   'beginHour', 'endHour',
                                   'TotalTimeSec', 'TotalTimeMin'])
   
    
    flight_id_num = len(states_df.groupby(level='flightId'))

    count = 0
    for flight_id, flight_id_group in states_df.groupby(level='flightId'):
        
        count = count + 1
        print(airport_icao, year, month, week, flight_id_num, count, flight_id)
        
        begin_date_str = states_df.loc[flight_id].head(1)['beginDate'].values[0]
        end_date_str = states_df.loc[flight_id].head(1)['endDate'].values[0]
        
        begin_timestamp = states_df.loc[flight_id]['timestamp'].values[0]
        begin_datetime = datetime.utcfromtimestamp(begin_timestamp)
        begin_hour_str = begin_datetime.strftime('%H')

        end_timestamp = states_df.loc[flight_id]['timestamp'].values[-1]
        end_datetime = datetime.utcfromtimestamp(end_timestamp)
        end_hour_str = end_datetime.strftime('%H')
        
        circle_50NM_time_sec = len(flight_id_group)     #seconds
        circle_50NM_time_min = len(flight_id_group)/60  #seconds to minutes
                
        pi_df = pd.concat([pi_df, pd.DataFrame({'flightId': [flight_id],
                                'beginDate': [begin_date_str], 
                                'endDate': [end_date_str],
                                'beginHour': [begin_hour_str],
                                'endHour': [end_hour_str],
                                'TotalTimeSec': [circle_50NM_time_sec],
                                'TotalTimeMin': [circle_50NM_time_min]})])

    pi_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)



def main():
    
    for week in range (0,4):
        calculate_50NM_time_by_flight(10, week+1)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))