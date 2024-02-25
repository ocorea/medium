"""created by: Orlin Corea
email: ocorea10@gmail.com / ocorea@truess.net
"""
import pandas as pd
from geopy import distance
from geopy.geocoders import Nominatim
import time
import numpy as np

#create the instance of Nominatim geocoders
geolocator = Nominatim(user_agent="medium_demo")

#region utility_functions
#auxiliary function to generate google map url, to visualize the location
def google_map_url(lat,lon):
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

#function to calculate the distance between two locations
# The factor represent the adjustment to the geodesic distance, to get a value more near to a road distance (Not lineal)
# the distance is returned in kilometers
def calculate_distance(lat_origin,lon_origin,lat_destiny,lon_destiny,factor=1.0):
    try:
        if (lat_origin and lon_origin and lat_destiny and lat_destiny):
            return distance.distance((lat_origin, lon_origin), (lat_destiny, lon_destiny)).km * factor
        else:
            return 0
     
    except Exception as e:
        print('Error in the process:',e)
        return 0

    
  

#function to get the latitude and longitude of the location
def get_lat_lon(country,city,street,zipcode):
    try:
        #adding a pause of at least 1 second to avoid the request being blocked
        time.sleep(1)
        if (zipcode is None):
            _query= f"{street}, {city}"
        else:
            _query= f"{zipcode}"
        location = geolocator.geocode(country_codes=[country], query=_query)
        if location:      
            latitude = location.latitude
            longitude = location.longitude        
            return latitude,longitude,google_map_url(latitude,longitude)
        else:
            return None,None,None
    except Exception as e:
        print('Error in the process:',e)
        return None,None,None
#endregion


        
#read the raw csv data source to get the location information
def process_location_data():
    #read the raw data
    df = pd.read_csv('./dataset/list_locations.csv',sep=';',dtype='str')
    #replace the NaN values with None in the imported dataframe
    df = df.replace(np.nan, None)
    #print the first 5 rows of the raw data
    print('---- Raw data to complement ----')
    print(df.head())

    #factor to adjust the geodesic distance to a road distance, if
    #the factor is 1.0, the distance is the geodesic distance, if the factor is 1.4, the distance is an aprox distance using road
    # in straight roads the real distance would be similar to the geodesic distance, but in curved roads, the distance would be greater (using a higher adjustment factor)
    ROAD_ESTIMATED_FACTOR = 1.35 

    for index, row in df.iterrows():
        #process the origin location
        df.at[index,'origin_latitude'],df.at[index,'origin_longitude'], df.at[index,'origin_google_map_url'] = get_lat_lon(row['origin_country'],
                                                                   row['origin_city'],
                                                                   row['origin_address'],
                                                         row['origin_zipcode'])
        #process the destiny location
        df.at[index,'destiny_latitude'],df.at[index,'destiny_longitude'], df.at[index,'destiny_google_map_url'] = get_lat_lon(row['destiny_country'],
                                                                   row['destiny_city'],
                                                                   row['destiny_address'],
                                                                     row['destiny_zipcode'])
        #calculate the distance between the origin and destiny location
        df.at[index,'distance_km'] = calculate_distance(df.at[index,'origin_latitude'],
                                                     df.at[index,'origin_longitude'],
                                                     df.at[index,'destiny_latitude'],
                                                     df.at[index,'destiny_longitude'],ROAD_ESTIMATED_FACTOR)       
        
 

                                                     
    #save the processed data
    print('---- Processed data result----')
    print(df.head())
    df.to_csv('./dataset/location_data_processed.csv',index=False)
    return True


#call the processing function
process_location_data()
