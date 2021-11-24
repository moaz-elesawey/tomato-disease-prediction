from pydantic import BaseModel
from typing import Optional


class PredictionBase(BaseModel):
    class_name  : str
    confidance  : float


class PredictionCreate(PredictionBase):
    pass


class Prediction(PredictionBase):
    id: int

