from fastapi import FastAPI
from starlette.responses import JSONResponse
from pydantic import BaseModel
app = FastAPI()

class Purchase(BaseModel):
    company : int
    user_id : int
    city : int

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