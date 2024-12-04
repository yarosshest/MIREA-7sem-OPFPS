from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, MIREA!"}

Instrumentator().instrument(app).expose(app)

