import numpy as np
import pandas as pd
import calendar
import os

AIRPORT_ICAO = "ENGM"

DATASETS = ["PM_NORTH", "PM_SOUTH", "TT_NORTH", "TT_SOUTH"]

import time
start_time = time.time()

DATA_DIR = os.path.join("data", AIRPORT_ICAO)
PIs_DIR = os.path.join(DATA_DIR, "PIs")


def calculate_hfe_by_hours(dataset):
    
    input_filename = dataset + "_PIs_horizontal_by_flights.csv"
    full_input_filename = os.path.join(PIs_DIR, input_filename)

    # 'flightId', 'beginDate', 'endDate', 'beginHour', 'endHour', 
    # 'referenceDistance', 'distanceTMA', 'additionalDistanceTMA', 'distanceChangePercent'
    hfe_by_flights_df = pd.read_csv(full_input_filename, sep=' ', dtype = {'endDate': str})

    hfe_by_hours_df = pd.DataFrame(columns=['date', 'hour', 'numberOfFlights', 
                            'additionalDistanceMean', 'additionalDistanceMedian',
                            'distanceChangePercentMean'
                            ])

    #print(hfe_by_flights_df.head())
    #p1 = hfe_by_flights_df["distanceChangePercent"].quantile(0.05)
    #p2 = hfe_by_flights_df["distanceChangePercent"].quantile(0.95)
    #hfe_by_flights_df = hfe_by_flights_df.loc[(hfe_by_flights_df['distanceChangePercent'] > p1) & (hfe_by_flights_df['distanceChangePercent'] < p2) ]
    
    hfe_by_flights_df.set_index(['endDate'], inplace=True)
    
    for date, date_df in hfe_by_flights_df.groupby(level='endDate'):
    
        print(date)
    
        for hour in range(0,24):
        
            hour_df = date_df[date_df['endHour'] == hour]

            number_of_flights_hour = len(hour_df)
            
            #remove outliers
            #if number_of_flights_hour>0:
            #    hour_df = hour_df.loc[(hour_df['distanceChangePercent'] > p1) & (hour_df['distanceChangePercent'] < p2) ]
            #    if len(hour_df)==0:
            #         number_of_flights_hour = 0
            
            if number_of_flights_hour == 0:
                average_additional_distance_hour = 0
                median_additional_distance_hour = 0
                average_distance_change_percent_hour = 0
                
            else:
                additional_distance_hour = hour_df['additionalDistance'].values # np array
            
                average_additional_distance_hour = np.mean(additional_distance_hour)
                median_additional_distance_hour = np.median(additional_distance_hour)
            
                distance_change_percent_hour = hour_df['distanceChangePercent'].values # np array
            
                average_distance_change_percent_hour = np.mean(distance_change_percent_hour)
              

            hfe_by_hours_df = pd.concat([hfe_by_hours_df, pd.DataFrame({
                                    'date': [date], 
                                    'hour': [hour],
                                    'numberOfFlights': [number_of_flights_hour],
                                    'additionalDistanceMean': [average_additional_distance_hour],
                                    'additionalDistanceMedian': [median_additional_distance_hour],
                                    'distanceChangePercentMean': [average_distance_change_percent_hour]})])

    return hfe_by_hours_df


def create_hfe_by_hours_file(dataset, hfe_by_hours_df):
    # not all dates in opensky states, creating empty rows for missing dates
    (nrows, ncol) = hfe_by_hours_df.shape

    month_date_list = []

    df_dates_np = hfe_by_hours_df.iloc[:,0].values
    
    date = '1910'

    for d in range(1,9):
        month_date_list.append(date + '0' + str(d))
    for d in range(10,29):
        month_date_list.append(date + str(d))

    for d in month_date_list:
        if d not in df_dates_np:
            for hour in range(0, 24):
                
                hfe_by_hours_df = pd.concat([hfe_by_hours_df, pd.DataFrame({
                                    'date': [date], 
                                    'hour': [hour],
                                    'numberOfFlights': [0],
                                    'additionalDistanceMean': [0],
                                    'additionalDistanceMedian': [0],
                                    'distanceChangePercentMean': [0]})])
                
                

    hfe_by_hours_df = hfe_by_hours_df.sort_values(by = ['date', 'hour'] )
    hfe_by_hours_df.reset_index(drop=True, inplace=True)

    #output_filename = "PIs_horizontal_by_hour.csv"
    output_filename = dataset + "PIs_horizontal_by_hours.csv"
    full_output_filename = os.path.join(PIs_DIR, output_filename)
    hfe_by_hours_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)



def main():
                    
    for dataset in DATASETS:
        
        hfe_by_hours_df = calculate_hfe_by_hours(dataset)
    
        create_hfe_by_hours_file(dataset, hfe_by_hours_df)
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))
