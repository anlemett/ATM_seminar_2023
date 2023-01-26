import pyproj

# no sign for lat because of 'N'
# no sign for lon because of 'E'
def dms2dd(as_string):
    degrees = int(as_string[:2])
    minutes = int(as_string[2:4])
    seconds = float(as_string[4:8])
    lat_dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    degrees = 1*int(as_string[11:14])
    minutes = 1*int(as_string[14:16])
    seconds = 1*float(as_string[16:21])
    lon_dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);

    return lat_dd, lon_dd;

# Runway 01L end COORD
# 601257.84N 0110529.99E
    
# Runway 19R end COORD
# 601106.00N 0110425.48E
    
# Runway 01R end COORD
# 601204.35N 0110720.95E
    
# Runway 19L end COORD
# 601032.72N 0110628.02E
    
rwy01L_end_lat, rwy01L_end_lon = dms2dd("601257.84N 0110529.99E")

rwy19R_end_lat, rwy19R_end_lon = dms2dd("601106.00N 0110425.48E")

rwy01R_end_lat, rwy01R_end_lon = dms2dd("601204.35N 0110720.95E")

rwy19L_end_lat, rwy19L_end_lon = dms2dd("601032.72N 0110628.02E")


rwy01L_lon=[rwy19R_end_lon, rwy01L_end_lon];
rwy01L_lat=[rwy19R_end_lat, rwy01L_end_lat];

rwy19R_lon=[rwy01L_end_lon, rwy19R_end_lon];
rwy19R_lat=[rwy01L_end_lat, rwy19R_end_lat];

rwy01R_lon=[rwy19L_end_lon, rwy01R_end_lon];
rwy01R_lat=[rwy19L_end_lat, rwy01R_end_lat];

rwy19L_lon=[rwy01R_end_lon, rwy19L_end_lon];
rwy19L_lat=[rwy01R_end_lat, rwy19L_end_lat];


geod = pyproj.Geod(ellps='WGS84')   # to determine runways via azimuth
#fwd_azimuth, back_azimuth, distance = geod.inv(lat1, long1, lat2, long2)

rwy01L_azimuth, rwy19R_azimuth, distance = geod.inv(rwy01L_lon[0], rwy01L_lat[0], rwy01L_lon[1], rwy01L_lat[1])

print(rwy01L_azimuth, rwy19R_azimuth, distance)

