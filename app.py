from src.exception import CustomException
from src.constants import *
from src.pipeline.train_pipeline import TrainingPipeline
from src.pipeline.prediction_pipeline import PredictionPipeline

from fastapi import FastAPI
from starlette.responses import RedirectResponse
from fastapi.responses import Response
import uvicorn
import sys


app = FastAPI()


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def training():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()

        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/predict")
async def predict_route(text):
    try:
        obj = PredictionPipeline()
        text = obj.run_pipeline(text)
        return text
    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
