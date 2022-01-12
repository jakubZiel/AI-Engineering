from pandas.core.frame import DataFrame
import requests as req
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from Purchase import Purchase
import sys
from pymongo import MongoClient 
from sklearn.metrics import classification_report

df = pd.read_json('../data/processed/casted_clearedDF.jsonl' , lines=True)

if __name__ == '__main__' :

    if len(sys.argv) != 2:
        test_size = 0.1
    else : 
        test_size = float(sys.argv[1])

    #prepare data
    df = df.drop(columns=[
        "delivery_company",
        "session_id",
        "purchase_timestamp", 
        "delivery_timestamp",
        "product_name",
        "price",
        "category_path",
        "week_day"
        ])

    label_city = LabelEncoder()
    df['city'] = label_city.fit_transform(df['city'])
    label_street = LabelEncoder()
    df['street'] = label_street.fit_transform(df['street'])

    x = df[['street', 'purchase_week_day_plus_hour', 'city', "user_id"]]
    y = df['delivery_time']

    #split data
    _, x_test, _, y_test = train_test_split(x, y, test_size = test_size, random_state = 0)

    number_of_requests = len(x_test)

    x_test : DataFrame = x_test

    #group y values for each test group
    test_group_a = []
    test_group_b = []
    
    for index, row in x_test.iterrows():
        if row['user_id'] % 2 == 0:
            test_group_a.append(y_test[index])
        else :
            test_group_b.append(y_test[index])


    x_test = x_test.values.tolist()
    
    #perform ab tests
    url = 'http://localhost:8000/ab_test?user_id='

    for i in range(0, number_of_requests):
        record = x_test[i]
        data = {
            'street' : record[0],
            'purchase_week_day_plus_hour' : record[1],
            'city' : record[2]
        }
        req.post(url + str(record[3]), json=data)

    #load the results
    db_server = MongoClient('localhost', 27017)

    group_a = db_server.get_database('ab_test').get_collection('group_a')
    group_b = db_server.get_database('ab_test').get_collection('group_b')

    predictions_a = []
    for ele_a in group_a.find():
        predictions_a.append(ele_a['prediction'])
    predictions_b = []
    for ele_b in group_b.find():
        predictions_b.append(ele_b['prediction'])


    #calculate quality metrics
    predictions_a = pd.Series(predictions_a)
    predictions_b = pd.Series(predictions_b)

    test_group_a = pd.Series(test_group_a)
    test_group_b = pd.Series(test_group_b)

