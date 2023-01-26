import pandas as pd
import os

year = '2019'
airport_icao = "ENGM"

months = ['10']

DATA_DIR = os.path.join("data", airport_icao)
WEATHER_DIR = os.path.join(DATA_DIR, "Weather")

filename = os.path.join(WEATHER_DIR, "ENGM_2019_10_wind_dir.csv")
wind_df = pd.read_csv(filename, sep=' ')

filename = os.path.join(DATA_DIR, "runways_by_hour.csv")
rwys_df = pd.read_csv(filename, sep=' ')

print(wind_df.head())
print(rwys_df.head())

df_inner = pd.merge(wind_df, rwys_df, on=['day', 'hour'], how='inner')
df_inner = df_inner[['day', 'hour', 'wind_dir_bool', 'flight_dir_bool']]


def sameBoolValue(a, b):
    
    return int(not bool(a) ^ bool(b))


df_inner['same'] = df_inner.apply(lambda row: sameBoolValue(row['wind_dir_bool'], row['flight_dir_bool']), axis=1)

print(df_inner.head())

filename = os.path.join(DATA_DIR, "compare_wind_runways_by_hour.csv")
df_inner.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)

same_df = df_inner[df_inner['same']==1]
dif_df = df_inner[df_inner['same']==0]

print(len(same_df))
print(len(dif_df))

# 80% - landing facing into the wind

