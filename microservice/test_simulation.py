from logging import root
from os import path
import requests
import pandas as pd
from sklearn.model_selection import train_test_split

root_address = 'http://localhost:8000'

df = pd.read_json('../data/processed/casted_clearedDF.jsonl' , lines=True)

df = df.drop(columns=[
    "delivery_company",
    "session_id",
    "user_id",
    "purchase_timestamp", 
    "delivery_timestamp",
    "product_name",
    "price",
    "category_path",
    "week_day"
    ])

x = df[['street', 'purchase_week_day_plus_hour', 'city']]
y = df['delivery_time']

_, x_test, _, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)


print(x_test)
print(y_test)