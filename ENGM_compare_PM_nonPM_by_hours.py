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

dataset = "nonPM"
PM_df = pd.read_csv(os.path.join(DATA_DIR, "PM_time_by_hour.csv"), sep=' ', dtype = {'date': str})
nonPM_df = pd.read_csv(os.path.join(DATA_DIR, "nonPM_time_by_hour.csv"), sep=' ', dtype = {'date': str})


df = pd.concat([PM_df, nonPM_df], axis=1)
df = pd.merge(PM_df, nonPM_df, on=['date', 'hour'], how='inner')


#print(df.head(1))


def greaterValue(a, b):
    
    return int(a>b)


df['greater'] = df.apply(lambda row: greaterValue(row['numberOfFlightsByStartAndEnd_x'], row['numberOfFlightsByStartAndEnd_y']), axis=1)


filename = os.path.join(DATA_DIR, "compare_PM_nonPM_by_hour.csv")
df.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)

greater_df = df[df['greater']==1]

greater_df = greater_df[['date', 'hour', 'numberOfFlightsByStartAndEnd_x', 'numberOfFlightsByStartAndEnd_y']]

greater_num = len(greater_df)

print(greater_num)

filename = os.path.join(DATA_DIR, "compare_PM_nonPM_greater_hours.csv")
greater_df.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)