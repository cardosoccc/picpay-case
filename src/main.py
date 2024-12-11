from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
from database import InMemoryDatabase
from uuid import uuid4
import os
import shutil
import pickle
from typing import Dict
import tempfile
from sklearn.base import BaseEstimator
from xgboost import XGBRegressor
import uvicorn
import numpy as np
from flight_data import FlightData
from preprocessor import preprocess, CosineEncoder

app = FastAPI()

db = InMemoryDatabase()
loaded_models: Dict[str, object] = {}


@app.get("/health", status_code=200, tags=["health"], summary="Health check")
async def health():
    return {"status": "ok"}


@app.post("/model/load", tags=["load"], summary="Load model")
async def load_model(file: UploadFile = File(...)):
    model_uuid = str(uuid4())
    models = db.get_collection('models')
    models.insert_one({"uuid": model_uuid, "status": "loading"})
    
    tmp_dir = tempfile.mkdtemp(suffix=model_uuid)
    file_path = os.path.join(tmp_dir, f'{model_uuid}.pkl')

    try:
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
            
        with open(file_path, 'rb') as f:
            model = pickle.load(f)

        if not isinstance(model, (BaseEstimator, XGBRegressor)):
            raise ValueError("The model is not a valid model.")
        
        loaded_models[model_uuid] = model
        models.update_one({'uuid': model_uuid}, {"$set": {'status': 'ready'}})
        response = models.find_one({'uuid': model_uuid})
        del response['_id']
        return response

    except Exception as e:
        shutil.rmtree(tmp_dir)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model/predict", status_code=200, tags=["predict"], summary="Get model predictions")
async def predict(uuid: str, flight_data: FlightData = Depends()):
    models = db.get_collection('models')
    model = models.find_one({'uuid': uuid})

    if not model:
        raise HTTPException(status_code=404, detail='Model not found')

    if model['status'] != 'ready':
        raise HTTPException(status_code=500, detail='Model not ready')

    try:
        loaded_model = loaded_models.get(uuid)
        if not loaded_model:
            tmp_dir = tempfile.mkdtemp(suffix=uuid)
            file_path = os.path.join(tmp_dir, f'{uuid}.pkl')
            with open(file_path, 'rb') as f:
                loaded_model = pickle.load(f)
                loaded_models[uuid] = loaded_model
        
        X = preprocess(flight_data)
        prediction = {
            "model_uuid": uuid,
            "input": flight_data,
            "prediction": float(loaded_model.predict(X)[0])
        }
        predictions = db.get_collection('predictions')
        predictions.insert_one(prediction)
        return prediction

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        
@app.get("/model/history", status_code=200, tags=["history"], summary="Get predicitions history")
async def predict(uuid: str):
    try:
        predictions = db.get_collection('predictions')
        return {"history": [prediction for prediction in predictions.find({'model_uuid': uuid})]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/model/unload", tags=["unload"], summary="Unload model")
async def unload_model(uuid: str = Form(...)):
    try:
        if uuid not in loaded_models:
            raise Exception(f"Model '{uuid}' not loaded.")
        
        del loaded_models[uuid]
        models = db.get_collection('models')
        models.update_one({'uuid': uuid}, {"$set": {'status': 'deleted'}})
        tmp_dir = tempfile.mkdtemp(suffix=uuid)
        shutil.rmtree(tmp_dir)
        return models.find_one({'uuid': uuid})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")