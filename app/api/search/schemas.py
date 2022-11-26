from pydantic import BaseModel, BaseConfig
from typing import Optional, List

class SearchResponseSchema(BaseModel):
    name: str
    gender: Optional[str] = None
    occupation: Optional[List] = []
    age: Optional[int] = None
    is_vip: Optional[bool] = None
    vip_score: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class SearchParamsSchema(BaseModel):
    name: str
    gender: str = None
    occupation: str = None
    age: int = None
    email: str = None


class SearchListSchema(BaseModel):
    data: List[SearchParamsSchema]
