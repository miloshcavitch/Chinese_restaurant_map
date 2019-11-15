import pandas as pd
df = pd.read_csv('chinese_data_nyc.csv', index_col=0)
#API picked up alot of duplicates, probably showing up in zip codes without a whole lot of chinese restaurants
df.drop_duplicates('formatted_address', inplace=True)

newFrame = zip(df['formatted_address'], df['geometry'], df['name'], df['price_level'], df['rating'], df['reference'], df['user_ratings_total'])

df_list = []
for addr,geo,name,price,rating,reference,user_ratings_total in newFrame:
    ray = [ addr,geo,name,price,rating,reference,user_ratings_total ]
    df_list.append(ray)
#creates a new dataframe with only needed columns as well as better names for the columns
df = pd.DataFrame(df_list, columns=['address', 'geometry', 'name', 'price_level', 'rating', 'reference', 'total_ratings'])

#keep all letters, number and spaces but remove commas
df['address'] = df['address'].str.replace('[^a-zA-Z\s0-9]', '')
#split the address by spaces
df['zip'] = df['address'].str.split(' ')

zips = []

for ray in df['zip']:
    zip = 0
    #iterate through the address, looking for the zip code
    for i, string in enumerate(ray):
        #if below is true, this is the zip code
        if ray[i-1] == 'NY' and len(string) == 5 and string.isdigit():
            zip = int(string)
    zips.append(zip)
#reset the zip column to be just the zip code
df['zip'] = pd.Series(zips)

df = df[df['zip'] != 0]

df.to_csv('chinese_data_clean.csv')
