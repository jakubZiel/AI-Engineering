import pymongo 
from pymongo import MongoClient
from pymongo import collection
import logging, coloredlogs
from pymongo.database import Database
from Purchase import Purchase
from typing import List, Dict

coloredlogs.install()


class TestArchive():
    db_server : MongoClient
    collections : Dict[str, collection.Collection] 
    
    def __init__(self):
        self.db_server = MongoClient('localhost', 27017)
        collection_cursor = self.db_server['ab_test'].list_collections()
        
        self.collections = {}

        for collection in collection_cursor:
            self.collections[collection['name']] = collection

    def insert_result(self, purchase : Purchase, prediction : int, group : str) -> None: 

        gen = self.db_server['ab_test'].get_collection('generator').find_one({"_id" : 0})
        self.db_server['ab_test'].get_collection('generator').update_one({"_id" : 0}, {"$inc" : {"next_id" : 1}})


        document = {
            '_id' : gen['next_id'],   
            'prediction' : int(prediction),
            'purchase' : purchase.__dict__
        }

        self.db_server['ab_test'].get_collection(group).insert_one(document)


if __name__ == "__main__" :
    db_server = MongoClient('localhost', 27017)

    if 'group_a' not in db_server['ab_test'].list_collection_names():
        db_server['ab_test'].create_collection('group_a')
    else :
        logging.warning('group a already exists in ab_test')

    if 'group_b' not in db_server['ab_test'].list_collection_names():
        db_server['ab_test'].create_collection('group_b')
    else :
        logging.warning('group b already exists in ab_test')

    if 'generator' not in db_server['ab_test'].list_collection_names():
        db_server['ab_test'].create_collection('generator')
        db_server['ab_test'].get_collection('generator').insert_one({'_id' : 0, "next_id" : 0})
    else :
        logging.warning('id generator already exists in ab_test')

