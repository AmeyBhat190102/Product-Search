from fastapi import FastAPI, Request, Response, HTTPException  # type: ignore

from app.logger import app_logger as logging
from app.utils import filter_by_embedding
from app.prompting import get_product_validity_wrt_request
from app.config import settings
from app.models import SearchRequestRequestModel, ProductResultResponseModel
from typing import List

import httpx  # type: ignore

app = FastAPI()


@app.post(
    "/v0/products/product-search-request",
    response_model=List[ProductResultResponseModel],
)
async def search_product(
    request: Request, response: Response, data: SearchRequestRequestModel
):
    try:
        user_query = data.query

        params = {
            "q": user_query,
            "gl": data.country.lower(),
            "hl": "en",
            "tbm": "shop",
            "api_key": settings.SERP_API_KEY.get_secret_value(),
        }

        async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
            response = await client.get(settings.SERP_API_ENDPOINT, params=params)
            products = response.json()

        results = []

        for item in products["shopping_results"]:
            results.append(
                {
                    "product_name": item["title"],
                    "price": item["extracted_price"],
                    "link": item["product_link"],
                    "source": item["source"],
                    "delivery": item.get("delivery", "Delivery Info is not Available"),
                    "reviews": item.get("reviews", "No reviews found for this Product"),
                    "ratings": item.get("rating", "No ratings found for this Product"),
                }
            )

        results = filter_by_embedding(query=user_query, products=results)
        revised_products = get_product_validity_wrt_request(
            user_query=user_query, products=results
        )

        return revised_products
    except Exception as e:
        logging.info(f"An Error Occured : {str(e)}")
        raise HTTPException(
            status_code=500, detail="An error occured while processing your request"
        )
