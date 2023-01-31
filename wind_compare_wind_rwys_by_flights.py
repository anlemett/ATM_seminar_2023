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


def getRwyDir(rwy): 
   
    if rwy == '01R' or rwy == '01L':
        return 1 # north
    else:
        return 0 # south
   
df['flight_dir_bool'] = df.apply(lambda row: getRwyDir(row['runway']), axis=1)    


WEATHER_DIR = os.path.join(DATA_DIR, "Weather")

#filename = os.path.join(WEATHER_DIR, "ENGM_2019_10_wind_dir.csv")
filename = os.path.join(WEATHER_DIR, "ENGM_2019_10_wind_dir_rwy.csv")
wind_df = pd.read_csv(filename, sep=' ')


df_inner = pd.merge(wind_df, df, on=['day', 'hour'], how='inner')
df_inner = df_inner[['day', 'hour', 'wind_dir_bool', 'flight_dir_bool']]


def sameBoolValue(a, b):
    
    return int(not bool(a) ^ bool(b))


df_inner['same'] = df_inner.apply(lambda row: sameBoolValue(row['wind_dir_bool'], row['flight_dir_bool']), axis=1)

print(df_inner.head())

filename = os.path.join(DATA_DIR, "compare_wind_runways_by_flight.csv")
df_inner.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)

same_df = df_inner[df_inner['same']==1]
dif_df = df_inner[df_inner['same']==0]


same_dir_num = len(same_df)
dif_dir_num = len(dif_df)

same_dir_percent = same_dir_num/(same_dir_num + dif_dir_num)
dif_dir_percent = dif_dir_num/(same_dir_num + dif_dir_num)
print(same_dir_percent)
print(dif_dir_percent)

# 85% - landing facing into the wind (wind near the runways)

