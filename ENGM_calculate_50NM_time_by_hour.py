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

def calculate_50NM_time_by_hour(month, week):
    input_filename = "PIs_50NM_time_by_flight_" + year + '_' +  str(month) + "_week" + str(week)+ ".csv"
    output_filename = "PIs_50NM_time_by_hour_" + year + '_' +  str(month) + "_week" + str(week)+ ".csv"


    #flight_id begin_date end_date begin_hour end_hour 50NM_time
    pi_df = pd.read_csv(os.path.join(DATA_DIR, input_filename), sep=' ', dtype = {'begin_date': str, 'end_date': str})

    pi_df.set_index(['end_date'], inplace=True)

    pi_by_hour_df = pd.DataFrame(columns=['date', 'hour',
                             'number_of_flights_by_end',
                             'number_of_flights_by_start_and_end',
                             '50NM_time_mean_sec',
                             '50NM_time_mean_min'
                             ])

    number_of_flights_by_hour_df = pd.DataFrame(columns=['date', 'hour', 'number_of_flights'])

    flight_id_list = []
    for date, date_df in pi_df.groupby(level='end_date'):
    
        print(date)
    
        for hour in range(0,24):
        
            hour_df = date_df[date_df['end_hour'] == hour]

            number_of_flights_hour= len(hour_df)
            
            hour_by_start_and_end_df = date_df[(date_df['end_hour'] == hour) | ((date_df['end_hour'] != hour) & (date_df['begin_hour'] == hour)) ]

            number_of_flights_hour_by_start_and_end = len(hour_by_start_and_end_df)

        
            time_50NM_hour = hour_by_start_and_end_df['50NM_time_sec'].values # np array

            time_50NM_hour_sum = np.sum(time_50NM_hour)

            average_time_50NM_hour = time_50NM_hour_sum/len(time_50NM_hour) if time_50NM_hour.any() else 0
                    
            pi_by_hour_df = pd.concat([pi_by_hour_df, pd.DataFrame({'date': [date],
                                    'hour': [hour], 
                                    'number_of_flights_by_end': [number_of_flights_hour],
                                    'number_of_flights_by_start_and_end': [number_of_flights_hour_by_start_and_end],
                                    '50NM_time_mean_sec': [average_time_50NM_hour],
                                    '50NM_time_mean_min': [average_time_50NM_hour/60] })])


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
                                        'number_of_flights_by_end': [0],
                                        'number_of_flights_by_start_and_end': [0],
                                        '50NM_time_mean_sec': [0],
                                        '50NM_time_mean_min': [0] })])


    pi_by_hour_df = pi_by_hour_df.sort_values(by = ['date', 'hour'] )
    pi_by_hour_df.reset_index(drop=True, inplace=True)

    pi_by_hour_df.to_csv(os.path.join(DATA_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)


def main():
    
    for week in range (0,4):
        calculate_50NM_time_by_hour(10, week+1)
    
    
main()    


print("--- %s minutes ---" % ((time.time() - start_time)/60))