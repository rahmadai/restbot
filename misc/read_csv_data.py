import pandas as pd

# df = pd.read_csv('/Users/rahmad/work/freelance-new/restbot/db/word_changes.csv')

# text = "halo tolong rekomendasi restoran yang ada parkiran"

# # run word by word inside text and replace with word_changes.csv
# for word in text.split():
#     try:
#         text = text.replace(word, df.loc[df['word'] == word, 'changes_word'].iloc[0])
#     except:
#         pass

# print(text)

# list = pd.read_csv('/Users/rahmad/work/freelance-new/restbot/db/list.csv')
# menu = pd.read_csv('/Users/rahmad/work/freelance-new/restbot/db/menu.csv')

# list['retaurant_name'] = list['retaurant_name'].str.lower()
# menu['retaurant_name'] = menu['retaurant_name'].str.lower()

# join list and menu table on retaurant_name and nama_resto

# Merge DataFrames and filter rows where the indicator column is 'left_only'
# list = list.merge(menu, on='retaurant_name', how='left', indicator=True)
# not_in_second_df = list[list['_merge'] == 'left_only']

# print(not_in_second_df)

# print merged_df for retaurant_name = tio ciu seafood & chinese food

# print(list.loc[list['retaurant_name'] == 'tio ciu seafood & chinese food'])


df = pd.read_csv('/Users/rahmad/work/freelance-new/restbot/db/list.csv')
df_location = pd.read_csv('/Users/rahmad/work/freelance-new/restbot/db/location_dataset.csv')
menu_df = pd.read_csv('/Users/rahmad/work/freelance-new/restbot/db/menu.csv')
menu_df['restaurant_name_lower'] = menu_df['nama_resto'].str.lower()
# lowercase df_location
df_location['location_name'] = df_location['location_name'].apply(lambda x: x.lower())
# df = preprocessing(df)
df['restaurant_name_lower'] = df['retaurant_name'].str.lower()
df = df.assign(category=df['category'].str.split(',')).explode('category')
df = df.assign(facility=df['facility'].str.split(',')).explode('facility')

df = df.merge(menu_df, on='restaurant_name_lower', how='left', indicator=True)

# print menu column if the restaurant_name_lower = 'tio ciu seafood & chinese food'
print(df.loc[df['restaurant_name_lower'] == 'tilasawa', 'menu'])