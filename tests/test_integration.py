from fastapi.testclient import TestClient
from main import app
from main import db

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_not_ready():
    response = client.get('/model/predict?uuid=1&month=12&wind_spd=1.1&distance=200&carrier=AA&hour=1&day=10&year=2024')
    assert response.status_code == 404

def test_predict_not_ready():
    models = db.get_collection('models')
    models.insert_one({"uuid": "1", "status": "loading"})

    response = client.get('/model/predict?uuid=1&month=12&wind_spd=1.1&distance=200&carrier=AA&hour=1&day=10&year=2024')
    assert response.status_code == 500
    assert response.json()['detail'] == 'Model not ready'

