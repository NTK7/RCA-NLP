import pandas as pd

df = pd.read_csv('data/data.csv')
df.head()

# drop the google_id and place_id columns
df.drop(['google_id', 'place_id'], axis=1, inplace=True)