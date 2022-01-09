from fastapi import FastAPI
from starlette.responses import JSONResponse
from Purchase import Purchase
from joblib import load
import os
import uvicorn

models_dir = "models/"

app = FastAPI()

if __name__ == "__main__" :
    model_files = os.listdir("models")
    models = {}
    model_names = {}

    for index, file in  enumerate(model_files):
        models[index] = load(models_dir + file)
        model_names[index] = file.split('.')[0] 
        
    @app.get("/ab_test")
    async def ab_test() -> JSONResponse:
        
        return {
            "a_accuracy" : 0.45,
            "b_accuracy" : 0.55
        }

    @app.post("/predict")
    async def predict(purchase : Purchase) -> JSONResponse:

        return {
            "prediction" : 0
        }

    @app.get("/models")
    async def all_models():
        return model_names

    uvicorn.run(app)
