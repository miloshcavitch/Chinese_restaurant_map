import geopandas as gpd
import geojsonio as gjio
import requests, json
import pandas as pd

api_key = '***************************************'
zips = gpd.read_file('zip_bounds.geojson')
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"


INPUT_STRING = 'chinese restaurant '

frames = []
for zip in zips['postalCode']:
    query = INPUT_STRING + zip
    print(query)
    r = requests.get(url + 'query=' + query + '&key=' + api_key)
    results = r.json()
    df = pd.DataFrame(results['results'])
    frames.append(df)
    print(len(frames))


final_df = pd.concat(frames)
final_df.to_csv('chinese_data_nyc.csv')
