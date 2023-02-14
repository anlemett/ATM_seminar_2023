import numpy as np
import pandas as pd
import os

AIRPORT_ICAO = "ENGM"

DATASETS = ["TT_final", "PM_final", "nonPM_final"]

import time
start_time = time.time()

DATA_DIR = os.path.join("data", AIRPORT_ICAO)
PIs_DIR = os.path.join(DATA_DIR, "PIs")

if not os.path.exists(DATA_DIR):
    print("NO DIR 1")

if not os.path.exists(PIs_DIR):
    print("NO DIR 2")


def calculate_vfe_by_hours(dataset):
    
    input_filename = dataset + "_PIs_vertical_by_flights.csv"
    full_input_filename = os.path.join(PIs_DIR, input_filename)

    # 'flightId',  'beginDate', 'endDate', 'beginHour', 'endHour',
    # 'numberOfLevels', 'timeOnLevels', 'timeOnLevelsPercent', 'timeTMA', 'cdoAltitude'    
    vfe_by_flights_df = pd.read_csv(full_input_filename, sep=' ', dtype = {'endDate': str})

    vfe_by_hours_df = pd.DataFrame(columns=['date', 'hour', 'numberOfFlights', 'numberOfLevelFlights',
                             'percentOfLevelFlights',
                             'numberOfLevelsTotal', 'numberOfLevelsMean', 'numberOfLevelsMedian',
                             'timeOnLevelsTotal', 'timeOnLevelsMean', 'timeOnLevelsMedian',
                             'timeOnLevelsMin', 'timeOnLevelsMax',
                             'timeOnLevelsPercentMean', 'timeOnLevelsPercentMedian',
                             'TMATimeMean', 'TMATimeMedian',
                             'cdoAltitudeMean', 'cdoAltitudeMedian'
                             ])
    
    
    vfe_by_flights_df.set_index(['endDate'], inplace=True)


    for date, date_df in vfe_by_flights_df.groupby(level='endDate'):
    
        print(date)
    
        for hour in range(0,24):
        
            hour_df = date_df[date_df['endHour'] == hour]

            number_of_flights_hour = len(hour_df)
            

            if number_of_flights_hour == 0:
                number_of_level_flights_hour = 0
                percent_of_level_flights_hour = 0
                total_number_of_levels_hour = 0
                average_number_of_levels_hour = 0
                median_number_of_levels_hour = 0
                total_time_on_levels_hour = 0
                average_time_on_levels_hour = 0
                median_time_on_levels_hour = 0
                min_time_on_levels_hour = 0
                max_time_on_levels_hour = 0
                average_time_on_levels_percent_hour = 0
                median_time_on_levels_percent_hour = 0
                average_time_TMA_hour = 0
                median_time_TMA_hour = 0
                average_cdo_altitude_hour = 0
                median_cdo_altitude_hour = 0
                
            else:
            
                level_df = hour_df[hour_df['numberOfLevels']>0]

                number_of_level_flights_hour = len(level_df)
        
                percent_of_level_flights_hour = number_of_level_flights_hour/number_of_flights_hour
        

                number_of_levels_hour = hour_df['numberOfLevels'].values # np array

                total_number_of_levels_hour = np.sum(number_of_levels_hour)

                average_number_of_levels_hour = total_number_of_levels_hour/len(number_of_levels_hour)
        
                median_number_of_levels_hour = np.median(number_of_levels_hour)
        

                time_on_levels_hour = hour_df['timeOnLevels'].values # np array
        
                total_time_on_levels_hour = round(np.sum(time_on_levels_hour), 3)
        
                average_time_on_levels_hour = total_time_on_levels_hour/len(time_on_levels_hour)
        
                median_time_on_levels_hour = np.median(time_on_levels_hour)
        
                min_time_on_levels_hour = round(np.min(time_on_levels_hour), 3)
        
                max_time_on_levels_hour = round(np.max(time_on_levels_hour), 3)
            
            
                time_on_levels_percent_hour = hour_df['timeOnLevelsPercent'].values # np array
        
                average_time_on_levels_percent_hour = np.mean(time_on_levels_percent_hour)
            
                median_time_on_levels_percent_hour = np.median(time_on_levels_percent_hour)

        
                time_TMA_hour = hour_df['timeTMA'].values # np array

                time_TMA_hour_sum = np.sum(time_TMA_hour)

                average_time_TMA_hour = time_TMA_hour_sum/len(time_TMA_hour)
        
                median_time_TMA_hour = np.median(time_TMA_hour)


                cdo_altitude_hour = hour_df['cdoAltitude'].values # np array
        
                total_cdo_altitude_hour = round(np.sum(cdo_altitude_hour), 3)
        
                average_cdo_altitude_hour = total_cdo_altitude_hour/len(cdo_altitude_hour)
        
                median_cdo_altitude_hour = np.median(cdo_altitude_hour)
        
            
            vfe_by_hours_df = pd.concat([vfe_by_hours_df, pd.DataFrame({
                                    'date': [date], 
                                    'hour': [hour],
                                    'numberOfFlights': [number_of_flights_hour],
                                    'percentOfLevelFlights': [percent_of_level_flights_hour],
                                    'numberOfLevelsTotal': [total_number_of_levels_hour],
                                    'numberOfLevelsMean': [average_number_of_levels_hour],
                                    'numberOfLevelsMedian': [median_number_of_levels_hour],
                                    'timeOnLevelsTotal': [total_time_on_levels_hour],
                                    'timeOnLevelsMean': [average_time_on_levels_hour],
                                    'timeOnLevelsMedian': [median_time_on_levels_hour],
                                    'timeOnLevelsMin': [min_time_on_levels_hour], 'timeOnLevelsMax': [max_time_on_levels_hour],
                                    'timeOnLevelsPercentMean': [average_time_on_levels_percent_hour],
                                    'timeOnLevelsPercentMedian': [median_time_on_levels_percent_hour],
                                    'TMATimeMean': [average_time_TMA_hour],
                                    'TMATimeMedian': [median_time_TMA_hour],
                                    'cdoAltitudeMean': [average_cdo_altitude_hour],
                                    'cdoAtitudeMedian': [median_cdo_altitude_hour]
                                    })])
            
    return vfe_by_hours_df


def create_vfe_by_hours_file(dataset, vfe_by_hours_df):
    # not all dates in opensky states, creating empty rows for missing dates
    (nrows, ncol) = vfe_by_hours_df.shape

    month_date_list = []

    df_dates_np = vfe_by_hours_df.iloc[:,0].values
    
    date = '1910'

    for d in range(1,10):
        month_date_list.append(date + '0' + str(d))
    for d in range(10,29):
        month_date_list.append(date + str(d))

    for d in month_date_list:
        if d not in df_dates_np:
            for hour in range(0, 24):
                
                vfe_by_hours_df = pd.concat([vfe_by_hours_df, pd.DataFrame({
                                    'date': [d], 
                                    'hour': [hour],
                                    'numberOfFlights': [0],
                                    'numberOfLevelsTotal': [0],
                                    'numberOfLevelsMean': [0],
                                    'numberOfLevelsMedian': [0],
                                    'timeOnLevelsTotal': [0],
                                    'timeOnLevelsMean': [0],
                                    'timeOnLevelsMedian': [0],
                                    'timeOnLevelsMin': [0], 'timeOnLevelsMax': [0],
                                    'timeOnLevelsPercentMean': [0],
                                    'timeOnLevelsPercentMedian': [0],
                                    'TMATimeMean': [0],
                                    'TMATimeMedian': [0],
                                    'cdoAltitudeMean': [0],
                                    'cdoAltitudeMedian': [0]
                                    })])
                
    vfe_by_hours_df = vfe_by_hours_df.sort_values(by = ['date', 'hour'] )
    vfe_by_hours_df.reset_index(drop=True, inplace=True)

    output_filename = dataset + "_PIs_vertical_by_hours.csv"
    full_output_filename = os.path.join(PIs_DIR, output_filename)
    vfe_by_hours_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)


def main():
    
    for dataset in DATASETS:
        
        vfe_by_hours_df = calculate_vfe_by_hours(dataset)
    
        create_vfe_by_hours_file(dataset, vfe_by_hours_df)
    
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))