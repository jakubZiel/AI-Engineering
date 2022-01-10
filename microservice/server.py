from fastapi import FastAPI, HTTPException
from pydantic.main import BaseModel
from starlette.responses import HTMLResponse, JSONResponse
from Purchase import Purchase
from joblib import load
import os
import uvicorn
from sklearn import base

models_dir = "models/"

app = FastAPI()

test_on = True

if __name__ == "__main__" :
    model_files = os.listdir("models")
    models = {}
    model_names = {}

    for index, file in  enumerate(model_files):
        models[index] = load(models_dir + file)
        model_names[index] = file.split('.')[0] 
        
    @app.post("/ab_test")
    async def ab_test() -> JSONResponse:
        
        if not test_on:
            raise HTTPException(status_code=400, detail="A/B test is not on.")

        return {
            "a_accuracy" : 0.45,
            "b_accuracy" : 0.55
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

    uvicorn.run(app)
