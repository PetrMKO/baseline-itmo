from typing import List, Union

from pydantic import BaseModel, HttpUrl


class PredictionRequest(BaseModel):
    id: int
    query: str


class PredictionResponse(BaseModel):
    id: int
    answer: Union[int, None]
    reasoning: str
    sources: List[HttpUrl]
