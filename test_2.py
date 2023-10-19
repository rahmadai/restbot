import pandas as pd
import json


df = pd.read_csv('design.csv')

print(df['menu'][0])

a = json.loads(df["menu"][0])

print(a[0])