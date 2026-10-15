"""API iris : predit une espece et compte chaque prediction dans Redis."""

import os

import joblib
import redis
from fastapi import FastAPI, Query

MODEL_PATH = os.environ.get("MODEL_PATH", "/model/iris_model.joblib")
REDIS_HOST = os.environ.get("REDIS_HOST", "base")
COUNTER_KEY = "predictions"

app = FastAPI(title="API iris")
store = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

_bundle = None


def load_bundle():
    global _bundle
    if _bundle is None:
        _bundle = joblib.load(MODEL_PATH)
    return _bundle


@app.get("/predict")
def predict(
    sepal_length: float = Query(5.1),
    sepal_width: float = Query(3.5),
    petal_length: float = Query(1.4),
    petal_width: float = Query(0.2),
):
    bundle = load_bundle()
    sample = [sepal_length, sepal_width, petal_length, petal_width]
    species = bundle["target_names"][int(bundle["model"].predict([sample])[0])]
    total = store.incr(COUNTER_KEY)
    return {"espece": species, "mesures": sample, "predictions": total}


@app.get("/stats")
def stats():
    total = store.get(COUNTER_KEY)
    return {"predictions": int(total or 0)}
