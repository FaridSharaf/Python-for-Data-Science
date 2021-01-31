import pandas as pd
from datetime import datetime
import os
import json

# load json file into a list
records = [json.loads(line) for line in open("usa.gov_click_data.json")]
#convert the list to a dataframe
data = pd.json_normalize(records)

# getting web browser and operating systems information
data['web_browser'] = data['a'].str.split(" ", 2, expand = True)[0]   # Web Browser details
data['operating_sys'] = data['a'].str.split(" ", 2, expand = True)[1] # Operating Systems info

# clear OS data from non-characters
data['operating_sys'] = data['operating_sys'].replace(regex={r';':'',r'\(':'', r'\)':''})

# extract the URL the user comes from
data['from_URL'] = data['r'].str.split("\/", expand = True)[2]

# fill the direct links value
data['from_URL'].fillna('direct', inplace = True)
# extract the URL the user is headed to
data['to_URL'] = data['u'].str.split("\/", expand = True)[2]

# find the city from which the request is initiated
data['city'] = data['cy']

# track the longitude where the request was sent
data[['longitude', 'latitude']] = data['ll'].apply(pd.Series)

# Retrieve each city time zone
data['time_zone'] = data['tz']

# convert time_in and time_out to local timezone
data['time_in'] = data['t']
data['time_in'] = pd.to_datetime(data['time_in'], unit = 's').dt.tz_localize('UTC').dt.tz_convert('UTC')

data['time_out'] = data['hc']
data['time_out'] = pd.to_datetime(data['time_out'], unit = 's').dt.tz_localize('UTC').dt.tz_convert('UTC')

# drop old data from dataframe
data.drop(columns = ['a', 'c', 'nk', 'tz', 'gr', 'g', 'h', 'l', 'al', 'hh', 'r', 'u', 't',
       'hc', 'cy', 'll', '_heartbeat_', 'kw'], inplace = True)
data.dropna(inplace = True)

print("Rows available:", data.shape[0])

output_path = os.getcwd()

print("File output path:", output_path)

# convert dataframe to a CSV file
data.to_csv('USA Data from Bitly.csv', index = False)

input('Press Enter to exit')