import numpy as np
import pandas as pd
import geopandas as gpd
from descartes import PolygonPatch
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import ast
from color_func import autoRGB, valueLERP

#create plotting variables
fig = plt.figure()
ax = fig.gca()

#get restaurant data
df = pd.read_csv('chinese_data_clean.csv', index_col=0)
#get zipcode data
zips = gpd.read_file('zip_bounds.geojson')
#convert postal code column from string to integer
zips['postalCode'] = zips['postalCode'].astype(int)

#get the median restaurant rating for the whole city
city_median = df['rating'].median()


#create iterable zipper
zipper = zip(zips['postalCode'], zips['geometry'])
#iterate through every zipcode
for zip, geometry in zipper:
    #create dataframe of chinese restaurants in current zipcode
    zipdf = df[df['zip'] == zip]
    #median is equal to the median average rating for the restaurants in the zipcode
    median = zipdf['rating'].median()

    #the zip code dataframe I used contained a number of really tiny zipcodes, that I don't think are official or are maybe considered zip codes within a zip code?
    #anyway, I found that just skipping zip codes that didnt have any chinese restaurants was the best way to remove them from the study and final heat map.
    #that is done below
    if median == np.nan:
        print('####################')
        print(zip)
        continue
    if zipdf.shape[0] == 0:
        print('####################')
        print(zip)
        continue

    #we have our median for the zip code, now we lerp it to a value between 0 and 1 from its difference to the median of the city
    #valueLERP function is found in color_func.py
    color_position = valueLERP(median - city_median, -0.4, 0.4)
    color = ''
    #autoRGB function is found in color_func.py
    #as the median rating gets higher, the red channel increases from 0 and the green channel decreases from 255. Blue channel is a constant at 255
    #this color algorithm creates a nice looking heatmap
    color = autoRGB(color_position, 255-color_position, 255)
    #add the geometry of the zipcode with the color to the plot
    ax.add_patch(PolygonPatch(geometry, fc=color, ec=color, alpha=1 ))

    #now, plot the position for all the chinese restaurants in the zip code
    for x in zipdf['geometry']:
        dict = ast.literal_eval(x)
        ax.scatter(dict['location']['lng'], dict['location']['lat'], c='#ff0000', alpha=1, s=0.1, zorder=3)


patch_vals = []#patches are for the legend
for x in range(9):
    ex = x - 4
    number = (ex * -0.1)
    hex = valueLERP(number, -0.4, 0.4)
    color = autoRGB(255 - hex, hex, 255)

    patch_vals.append(mpatches.Patch(color=color, label=round(number * -1 ,2)))
patch_vals.reverse()
ax.legend(handles=patch_vals, title='(Zip Median Rating) - (City Median Rating)')
ax.axis('scaled')
plt.show()
