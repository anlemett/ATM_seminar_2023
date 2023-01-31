import pandas as pd
import os

from geopy.distance import geodesic

from datetime import datetime

import time
start_time = time.time()

year = '2019'

months = ['10']

AIRPORT_ICAO = "ENGM"

DATASETS = ["PM_NORTH", "PM_SOUTH", "TT_NORTH", "TT_SOUTH"]

#descent part ends at 1800 feet
descent_end_altitude = 1800 / 3.281

DATA_DIR = os.path.join("data", AIRPORT_ICAO)

INPUT_DIR = os.path.join(DATA_DIR, "Datasets")

CLUSTERS_DIR = os.path.join(DATA_DIR, "Clustering")
   
OUTPUT_DIR = os.path.join(DATA_DIR, "PIs")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    
REF_DIST_DIR = os.path.join(DATA_DIR, "PIs")
ref_filename = "ref_trajectories_distances.csv"
full_ref_filename = os.path.join(REF_DIST_DIR, ref_filename)
ref_df = pd.read_csv(full_ref_filename, sep=' ')


def get_all_states(dataset):

    input_filename =  dataset + ".csv"
    full_input_filename = os.path.join(INPUT_DIR, input_filename)

    df = pd.read_csv(full_input_filename, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':int, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
    
    df = df[['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'altitude', 'endDate']]
    
    # need for distance calculation but not for runway determination
    df = df[df['altitude']>descent_end_altitude]
    
    df.set_index(['flightId', 'sequence'], inplace=True)
    
    return df


def get_distance_ref(column, cluster):

    ref_lst = ref_df[column].to_list()
    distance_ref = float(ref_lst[cluster-1])
    return distance_ref


def calculate_horizontal_PIs(dataset):
           
    output_filename = dataset + "_PIs_horizontal_by_flights.csv"
    full_output_filename = os.path.join(OUTPUT_DIR, output_filename)

    states_df = get_all_states(dataset)
    
    number_of_flights = len(states_df.groupby(level='flightId'))
    print(number_of_flights)


    clusters_filename = dataset + "_clusters_6.csv"
    full_clusters_filename = os.path.join(CLUSTERS_DIR, clusters_filename)
    
    clusters_df = pd.read_csv(full_clusters_filename, sep=' ')
    clusters_df.set_index(['flight_id'], inplace=True)
    
        
    hfe_df = pd.DataFrame(columns=['flightId',
                                   'beginDate', 'endDate', 
                                   'beginHour', 'endHour', 
                                   'referenceDistance',
                                   'distance', 'additionalDistance', 'distanceChangePercent'
                                   ])

    
    flight_id_num = len(states_df.groupby(level='flightId'))

    count = 0
    for flight_id, flight_id_group in states_df.groupby(level='flightId'):
        
        count = count + 1
        print(AIRPORT_ICAO, dataset, flight_id_num, count, flight_id)

        begin_timestamp = states_df.loc[flight_id]['timestamp'].values[0]
        begin_datetime = datetime.utcfromtimestamp(begin_timestamp)
        begin_hour_str = begin_datetime.strftime('%H')
        begin_date_str = begin_datetime.strftime('%y%m%d')
        
        end_timestamp = states_df.loc[flight_id]['timestamp'].values[-1]
        end_datetime = datetime.utcfromtimestamp(end_timestamp)
        end_hour_str = end_datetime.strftime('%H')
        end_date_str = end_datetime.strftime('%y%m%d')

        distance_sum = 0

        #df_length = len(flight_id_group)
        
        for seq, row in flight_id_group.groupby(level='sequence'):
             
            if seq == 0:
                previous_point = (row['lat'].values[0], row['lon'].values[0])
                continue
            
            current_point = (row['lat'].values[0], row['lon'].values[0])
            
            distance_sum = distance_sum + geodesic(previous_point, current_point).meters
            previous_point = current_point


        distance_str = "{0:.3f}".format(distance_sum)

        # Calculate reference distance and additional distance based on cluster
        
        distance_ref = 0
        
        cluster = int(clusters_df.loc[flight_id]['cluster'])
        
        distance_ref = get_distance_ref(dataset, cluster)

        distance_sum = float(distance_sum * 0.000539957) # meters to NM
        distance_str = "{0:.2f}".format(distance_sum)
        #distance_ref = distance_ref * 1852     # NM to meters
         
        add_distance = distance_sum - distance_ref
        add_distance_str = "{0:.2f}".format(add_distance)
        
        distance_change_percent = (add_distance / distance_ref) * 100
        distance_change_percent_str = "{0:.2f}".format(distance_change_percent)
                      
        hfe_df = pd.concat([hfe_df, pd.DataFrame({'flightId': [flight_id],
                                'beginDate': [begin_date_str], 
                                'endDate': [end_date_str],
                                'beginHour': [begin_hour_str],
                                'endHour': [end_hour_str],
                                'referenceDistance': [distance_ref],
                                'distance': [distance_str],
                                'additionalDistance': [add_distance_str],
                                'distanceChangePercent': [distance_change_percent_str]
                                })])

    hfe_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)


def main():
    
    for dataset in DATASETS:
    
        calculate_horizontal_PIs(dataset)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))