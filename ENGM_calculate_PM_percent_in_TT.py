import pandas as pd
import os

AIRPORT_ICAO = "ENGM"

DATASETS = ["TT_final_NORTH", "TT_final_SOUTH", "PM_final_NORTH", "PM_final_SOUTH", "nonPM_final_NORTH", "nonPM_final_SOUTH"]

import time
start_time = time.time()

DATA_DIR = os.path.join("data", AIRPORT_ICAO)
PIs_DIR = os.path.join(DATA_DIR, "PIs")


input_filename = "TT_final_PIs_vertical_by_flights.csv"
full_input_filename = os.path.join(PIs_DIR, input_filename)

# 'flightId', 'beginDate', 'endDate', 'beginHour', 'endHour', 
# 'referenceDistance', 'distanceTMA', 'additionalDistanceTMA', 'distanceChangePercent'
TT_vfe_by_flights_df = pd.read_csv(full_input_filename, sep=' ', dtype = {'endDate': str})

input_filename = "PM_final_PIs_vertical_by_flights.csv"
full_input_filename = os.path.join(PIs_DIR, input_filename)

# 'flightId', 'beginDate', 'endDate', 'beginHour', 'endHour', 
# 'referenceDistance', 'distanceTMA', 'additionalDistanceTMA', 'distanceChangePercent'
PM_vfe_by_flights_df = pd.read_csv(full_input_filename, sep=' ', dtype = {'endDate': str})

input_filename = "nonPM_final_PIs_vertical_by_flights.csv"
full_input_filename = os.path.join(PIs_DIR, input_filename)

# 'flightId', 'beginDate', 'endDate', 'beginHour', 'endHour', 
# 'referenceDistance', 'distanceTMA', 'additionalDistanceTMA', 'distanceChangePercent'
nonPM_vfe_by_flights_df = pd.read_csv(full_input_filename, sep=' ', dtype = {'endDate': str})

TT_list = list(TT_vfe_by_flights_df["flightId"])
PM_list = list(PM_vfe_by_flights_df["flightId"])
nonPM_list = list(nonPM_vfe_by_flights_df["flightId"])

number_PM_in_TT = 0
number_nonPM_in_TT = 0

for flight_id in TT_list:
    if flight_id in PM_list:
        number_PM_in_TT = number_PM_in_TT + 1
    if flight_id in nonPM_list:
        number_nonPM_in_TT = number_nonPM_in_TT + 1
        
print(number_PM_in_TT)

print(number_PM_in_TT/len(TT_list))

print(number_nonPM_in_TT)

print(number_nonPM_in_TT/len(TT_list))

# 62% - nonPM, 38% - PM
