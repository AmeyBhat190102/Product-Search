from pydantic import BaseModel  # type: ignore
from typing import Any


class SearchRequestRequestModel(BaseModel):
    country: str
    query: str


class ProductValidationOutputModel(BaseModel):
    is_valid_product: bool
    reason: str


class LLMResponse(BaseModel):
    is_valid_product: bool
    reason: str


class ProductResultResponseModel(BaseModel):
    product_name: str
    price: int | float
    link: str
    source: str
    delivery: str
    reviews: Any
    ratings: Any
    similarity: float
    llm_response: LLMResponse
