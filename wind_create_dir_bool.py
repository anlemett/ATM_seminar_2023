import pandas as pd
import numpy as np
import os

# example
# 1 - north
# 2 - south
# 3 - east 
# 4 - west
# 5  - n-w
# 6 - n-e
# 7 - s-e
# 8 - s-w
U = np.array([[ 0.  ],
       [ 0.  ],
       [-1.  ],
       [1.  ],
       [ 1.  ],
       [-1.  ],
       [-1.  ],
       [ 1.  ]])

V = np.array([[ -1.  ],
       [ 1.  ],
       [ 0.  ],
       [ 0.  ],
       [-1.  ],
       [-1.  ],
       [ 1.  ],
       [ 1.  ]])

Dir=np.mod(180+np.rad2deg(np.arctan2(U, V)),360)
# Dir:
#[[  0.]
# [180.]
# [ 90.]
# [270.]
# [315.]
# [ 45.]
# [135.]
# [225.]]  

print(Dir)

year = '2019'
airport_icao = "ENGM"

months = ['10']

DATA_DIR = os.path.join("data", airport_icao)
WEATHER_DIR = os.path.join(DATA_DIR, "Weather")

filename = os.path.join(WEATHER_DIR, "ENGM_2019_10_wind_mean_by_lat_lon.csv")
wind_df = pd.read_csv(filename, sep=' ')

U = wind_df[["u100"]].to_numpy() 
V = wind_df[["v100"]].to_numpy() 

Dir=np.mod(180+np.rad2deg(np.arctan2(U, V)),360)

flat_list = [item for sublist in Dir.tolist() for item in sublist]
wind_df['wind_dir_degree'] = flat_list

def getWindDirBool(dir_degree): # direction of wind - FROM (not to)
    
    if (dir_degree >= 90+16) and (dir_degree<=270+16):
        return 0; # south
    else:
        return 1; # north
    
wind_df['wind_dir_bool'] = wind_df.apply(lambda row: getWindDirBool(row['wind_dir_degree']), axis=1)    

filename = os.path.join(WEATHER_DIR, "ENGM_2019_10_wind_dir.csv")
wind_df.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)

