from database import InMemoryDatabase

def test_insert():
  db = InMemoryDatabase()
  models = db.get_collection('models')
  uuid = "abc"
  models.insert_one({"uuid": uuid, "status": "loading"})
  model = models.find_one({'uuid': uuid})
  assert model['uuid'] == uuid

def test_update():
  db = InMemoryDatabase()
  models = db.get_collection('models')
  uuid = "abc"
  models.insert_one({"uuid": uuid, "status": "loading"})
  models.update_one({"uuid": uuid}, {"$set": {'status': 'ready'}})
  model = models.find_one({'uuid': uuid})
  assert model['status'] == 'ready'


def test_find():
  db = InMemoryDatabase()
  predictions = db.get_collection('predictions')
  predictions.insert_one({"model_uuid": 1, "prediction": 1.0})
  predictions.insert_one({"model_uuid": 2, "prediction": 2.0})
  predictions.insert_one({"model_uuid": 1, "prediction": 3.0})

  retrieved = [prediction for prediction in predictions.find({'model_uuid': 1})]

  assert len(retrieved) == 2
  assert all(r['model_uuid'] == 1 for r in retrieved)
  assert sum(r['prediction'] for r in retrieved) == 4
