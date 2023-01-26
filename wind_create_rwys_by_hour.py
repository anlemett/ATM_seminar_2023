import pandas as pd
import os

year = '2019'
airport_icao = "ENGM"

months = ['10']

DATA_DIR = os.path.join("data", airport_icao)

filename = os.path.join(DATA_DIR, "runways_2019_10_week1.csv")
rwys_week1_df = pd.read_csv(filename, sep=' ', dtype = {'date': str})

filename = os.path.join(DATA_DIR, "runways_2019_10_week2.csv")
rwys_week2_df = pd.read_csv(filename, sep=' ', dtype = {'date': str})

filename = os.path.join(DATA_DIR, "runways_2019_10_week3.csv")
rwys_week3_df = pd.read_csv(filename, sep=' ', dtype = {'date': str})

filename = os.path.join(DATA_DIR, "runways_2019_10_week4.csv")
rwys_week4_df = pd.read_csv(filename, sep=' ', dtype = {'date': str})

df = pd.concat([rwys_week1_df, rwys_week2_df, rwys_week3_df, rwys_week4_df])

def getDay(date): 
    
    return int(date[4:])
    
df['day'] = df.apply(lambda row: getDay(row['date']), axis=1)    

df.set_index(['day', 'hour'], inplace=True)



day = []
hour = []
rwy01R = []
rwy01L = []
rwy19R = []
rwy19L = []


for idx, hour_df in df.groupby(level=[0, 1]):

    day.append(idx[0])
    hour.append(idx[1])
    
    rwy01R.append(len(hour_df[hour_df['runway']=='01R']))
    rwy01L.append(len(hour_df[hour_df['runway']=='01L']))
    rwy19R.append(len(hour_df[hour_df['runway']=='19R']))
    rwy19L.append(len(hour_df[hour_df['runway']=='19L']))

rwys_number_df = pd.DataFrame()

rwys_number_df['day'] = day
rwys_number_df['hour'] = hour
rwys_number_df['01R'] = rwy01R
rwys_number_df['01L'] = rwy01L
rwys_number_df['19R'] = rwy19R
rwys_number_df['19L'] = rwy19L

print(rwys_number_df.head())

def getFlightDirBool(rwy01R, rwy01L, rwy19R, rwy19L): # direction of flight - TO (not from)
    
    if rwy01R + rwy01L > rwy19R + rwy19L:
        return 1; # north
    else:
        return 0; # south
    
rwys_number_df['flight_dir_bool'] = rwys_number_df.apply(lambda row: getFlightDirBool(row['01R'], row['01L'], row['19R'], row['19L']), axis=1)


filename = os.path.join(DATA_DIR, "runways_by_hour.csv")
rwys_number_df.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)

