import numpy as np
import pandas as pd
from calendar import monthrange
import os

import time
start_time = time.time()

year = '2019'
airport_icao = "ENGM"

months = ['10']

DATA_DIR = os.path.join("data", airport_icao)

DATA_DIR = os.path.join(DATA_DIR, "PIs")

dataset = "PM"

def calculate_50NM_time_by_hour(dataset):
    input_filename = dataset + "_time_by_flight.csv"
    output_filename = dataset + "_time_by_hour.csv"


    #flightId beginDate endDate beginHour endHour totalTimeSec totalTimeMin
    pi_df = pd.read_csv(os.path.join(DATA_DIR, input_filename), sep=' ', dtype = {'beginDate': str, 'endDate': str})

    pi_df.set_index(['endDate'], inplace=True)

    pi_by_hour_df = pd.DataFrame(columns=['date', 'hour',
                             'numberOfFlightsByEnd',
                             'numberOfFlightsByStartAndEnd',
                             'totalTimeMeanSec',
                             'totalTimeMeanMin'
                             ])


    for date, date_df in pi_df.groupby(level='endDate'):
    
        print(date)
    
        for hour in range(0,24):
        
            hour_df = date_df[date_df['endHour'] == hour]

            number_of_flights_hour= len(hour_df)
            
            hour_by_start_and_end_df = date_df[(date_df['endHour'] == hour) | ((date_df['endHour'] != hour) & (date_df['beginHour'] == hour)) ]

            number_of_flights_hour_by_start_and_end = len(hour_by_start_and_end_df)

        
            time_50NM_hour = hour_by_start_and_end_df['TotalTimeSec'].values # np array

            time_50NM_hour_sum = np.sum(time_50NM_hour)

            average_time_50NM_hour = time_50NM_hour_sum/len(time_50NM_hour) if time_50NM_hour.any() else 0
                    
            pi_by_hour_df = pd.concat([pi_by_hour_df, pd.DataFrame({'date': [date],
                                    'hour': [hour], 
                                    'numberOfFlightsByEnd': [number_of_flights_hour],
                                    'numberOfFlightsByStartAndEnd': [number_of_flights_hour_by_start_and_end],
                                    'totalTimeMeanSec': [average_time_50NM_hour],
                                    'totalTimeMeanMin': [average_time_50NM_hour/60] })])


    # not all dates in opensky states, creating empty rows for missing dates
    (nrows, ncol) = pi_by_hour_df.shape

    month_date_list = []


    df_dates_np = pi_by_hour_df.iloc[:,0].values

    for month in months:
        (first_day_weekday, number_of_days) = monthrange(int(year), int(month))
    
        date = year[2:] + month
        
        for d in range(1,9):
            month_date_list.append(date + '0' + str(d))
        for d in range(10,number_of_days+1):
            month_date_list.append(date + str(d))

    for d in month_date_list:
        if d not in df_dates_np:
            for hour in range(0, 24):
                
                pi_by_hour_df = pd.concat([pi_by_hour_df, pd.DataFrame({'date': [d],
                                        'hour': [hour], 
                                        'numberOfFlightsByEnd': [0],
                                        'numberOfFlightsByStartAndEnd': [0],
                                        'totalTimeMeanSec': [0],
                                        'totalTimeMeanMin': [0] })])


    pi_by_hour_df = pi_by_hour_df.sort_values(by = ['date', 'hour'] )
    pi_by_hour_df.reset_index(drop=True, inplace=True)

    pi_by_hour_df.to_csv(os.path.join(DATA_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)


def main():
    
    calculate_50NM_time_by_hour(dataset)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))