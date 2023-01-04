from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

from Services.LSTMPredictionService import LSTMPredictionService

#Prediction variables
LSTMNetworkService = LSTMPredictionService('./testing_0.h5', './komplet_dataset_backend_dictionaries', 127, 256)

#FastAPI variables
class Sentence(BaseModel):
    sentence: str

app = FastAPI()

#========== ENDPOINTS ==========
@app.get("/health")
async def get_health():
    return { "Status" : "Healthy" }

@app.post("/lstm/predict")
async def predict_sentence_lstm(request: Sentence):
    #TODO Make mock sentence work!
    return { "prediction" : LSTMNetworkService.inference(request.sentence) }

#========== ENDPOINTS ==========