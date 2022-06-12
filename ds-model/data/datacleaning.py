import pandas as pd

df = pd.read_csv('data/data.csv')
df.head()

# drop all the columns from the df expect 'review_text' and 'rating'
df = pd.read_csv('./data/data.csv')
df.drop(['google_id', 'place_id', 'location_link', 'reviews_link', 'reviews_per_score', 'review_id', 'author_link', 'author_title', 'author_id', 'name', 'author_image', 'review_img_url', 'owner_answer', 'owner_answer_timestamp', 'owner_answer_timestamp_datetime_utc', 'review_link', 'review_rating', 'review_timestamp', 'review_datetime_utc', 'review_likes', 'reviews_id'], axis=1, inplace=True)
df.head()

# getting the minimum and maximum values of the rating column
df['rating'].min()
df['rating'].max()


# get count of rows with the 'rating' less than 3
df[df['rating'] < 3].count()

# using the 'rating' column create a new column called label which is either 1 or 0 depending on the rating, 1 for positive and 0 for negative reviews and drop the 'rating' column from the df
df = pd.read_csv('./data/data.csv')
df['label'] = df['rating'].apply(lambda x: 1 if x > 3 else 0)
df.drop(['rating'], axis=1, inplace=True)
df.head()

# get total count of total label 1 and label 0
df['label'].value_counts()

# get reviews with label 0
df[df['label'] == 0]

# drop rows with review_text where NaN
df = pd.read_csv('./data/data.csv')
df.dropna(subset=['review_text'], inplace=True)
df.head()

# re index the rows of the df
df = pd.read_csv('./data/data.csv')
df.reset_index(drop=True, inplace=True)


# export the final df as a new csv file
df.to_csv('./data/data_cleaned.csv', index=False)




