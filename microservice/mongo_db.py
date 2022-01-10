import pymongo 
from pymongo import MongoClient
from pymongo import collection
import logging, coloredlogs

coloredlogs.install()

db_server = MongoClient('localhost', 27017)

if 'group_a' not in db_server['ab_test'].list_collection_names():
    db_server['ab_test'].create_collection('group_a')
else :
    logging.warning('group a already exists in ab_test')

if 'group_b' not in db_server['ab_test'].list_collection_names():
    db_server['ab_test'].create_collection('group_b')
else :
    logging.warning('group b already exists in ab_test')

