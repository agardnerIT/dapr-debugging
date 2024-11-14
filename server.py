
from fastapi import FastAPI

app = FastAPI()

@app.get("/foo")
def read_root():
    return {"Hello": "World"}
