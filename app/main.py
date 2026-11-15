
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI(title="Addition API")

DATA_FILE = "data/current.csv"


class AdditionInput(BaseModel):
    num1: float
    num2: float


def save_data(num1, num2, result):
    os.makedirs("data", exist_ok=True)

    record = pd.DataFrame([{
        "num1": num1,
        "num2": num2,
        "result": result
    }])

    record.to_csv(
        DATA_FILE,
        mode="a",
        header=not os.path.exists(DATA_FILE),
        index=False
    )


@app.get("/")
def home():
    return {
        "message": "Addition API is running successfully"
    }


@app.post("/add")
def addition(data: AdditionInput):

    result = data.num1 + data.num2

    save_data(data.num1, data.num2, result)

    return {
        "num1": data.num1,
        "num2": data.num2,
        "operation": "Addition",
        "result": result
    }
