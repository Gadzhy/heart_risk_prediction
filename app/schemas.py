from pydantic import BaseModel

class PredictionResult(BaseModel):
    id: int
    prediction: int