from re import T
from fastapi import FastAPI, HTTPException
from pydantic.main import BaseModel
from pymongo.auth import _xor
from starlette.responses import HTMLResponse, JSONResponse
from Purchase import Purchase
from joblib import load
import os
import uvicorn
from sklearn import base

from mongo_db import TestArchive

models_dir = "../models/"

app = FastAPI()

testArchive = TestArchive()

test_on = True


if __name__ == "__main__" :
    model_files = os.listdir(models_dir)
    models = {}
    model_names = {}

    os.system("python3 ./mongo_db.py")

    for index, file in  enumerate(model_files):
        models[index] = load(models_dir + file)
        model_names[index] = file.split('.')[0] 
        
    @app.post("/ab_test")
    async def ab_test(purchase : Purchase, user_id : int) -> JSONResponse:
        global test_on

        if not test_on:
            raise HTTPException(status_code=400, detail="A/B test is not on.")

        group = 'group_a' if user_id % 2 == 0 else 'group_b'
        group_id = user_id % 2

        prediction = models[group_id].predict([purchase.toVector()])[0]
    
        testArchive.insert_result(purchase, prediction, group)

        return {
            "response" : "OK",
            "group" : group
        }

    @app.post("/predict/{model_id}")
    async def predict(model_id : int, purchase : Purchase) -> JSONResponse:        
        
        if model_id not in models:
            raise HTTPException(status_code=404, detail="Model id " + str(model_id) + " doesn't exist")
        if purchase is None:
            raise HTTPException(status_code=400, detail="Request can't be empty")   
        
        return {
            "prediction" : int(models[model_id].predict([purchase.toVector()])[0])
        }

    @app.get("/models")
    async def all_models() -> JSONResponse:
        return model_names

    @app.post("/ab_test_switch")
    async def switch(turned_on : bool):
        global test_on
        switched = test_on ^ turned_on
        test_on = turned_on
        
        return {
            'ab_test_state' : test_on,
            'switched?' : switched
        }

    uvicorn.run(app)
