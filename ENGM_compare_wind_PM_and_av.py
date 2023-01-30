import pandas as pd
import os

year = '2019'
airport_icao = "ENGM"

months = ['10']

DATA_DIR = os.path.join("data", airport_icao)
PI_DIR = os.path.join(DATA_DIR, "PIs")
WEATHER_DIR = os.path.join(DATA_DIR, "Weather")

filename = os.path.join(WEATHER_DIR, "ENGM_2019_10_wind_dir_rwy.csv")
wind_df = pd.read_csv(filename, sep=' ')

av = wind_df['wind100'].mean()

#print(av)

def changeDateToDay(date):
    return date-191000

def greaterValue(a, b):
    
    return int(a>b)



# Take only hours when the number of flights in PM dataset greter than in nonPM dataset
filename = os.path.join(PI_DIR, "compare_PM_nonPM_greater_hours.csv")
PM_greater_df = pd.read_csv(filename, sep=' ')

PM_greater_df['day'] = PM_greater_df.apply(lambda row: changeDateToDay(row['date']), axis=1)

df_inner = pd.merge(wind_df, PM_greater_df, on=['day', 'hour'], how='inner')
df_inner = df_inner[['day', 'hour', 'wind100']]


df_inner['wind_greater_av'] = df_inner.apply(lambda row: greaterValue(row['wind100'], av), axis=1)


filename = os.path.join(PI_DIR, "compare_wind_PM_and_av_by_hour1.csv")
df_inner.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)

greater_av_df = df_inner[df_inner['wind_greater_av']==1]

greater_av_num = len(greater_av_df)
PM_greater_num = len(PM_greater_df)

greater_av_percent = greater_av_num/PM_greater_num

print(greater_av_percent)


# Take only hours when the number of flights in PM dataset is greater than 0
filename = os.path.join(PI_DIR, "PM_time_by_hour.csv")
PM_df = pd.read_csv(filename, sep=' ')

PM_df['day'] = PM_df.apply(lambda row: changeDateToDay(row['date']), axis=1)

PM_df = PM_df[PM_df['numberOfFlightsByStartAndEnd']>0]

df_inner = pd.merge(wind_df, PM_df, on=['day', 'hour'], how='inner')
df_inner = df_inner[['day', 'hour', 'wind100']]


df_inner['wind_greater_av'] = df_inner.apply(lambda row: greaterValue(row['wind100'], av), axis=1)


filename = os.path.join(PI_DIR, "compare_wind_PM_and_av_by_hour2.csv")
df_inner.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)

greater_av_df = df_inner[df_inner['wind_greater_av']==1]

greater_av_num = len(greater_av_df)
PM_num = len(PM_df)

greater_av_percent = greater_av_num/PM_num

print(greater_av_percent)

