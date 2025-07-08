from langchain_openai import ChatOpenAI  # type: ignore
from langchain.prompts import PromptTemplate  # type: ignore
from langchain.output_parsers import PydanticOutputParser  # type: ignore
from app.config import settings
from app.models import ProductValidationOutputModel


llm = ChatOpenAI(
    model=settings.LANGCHAIN_MODEL,
    temperature=settings.LANGCHAIN_TEMP,
    max_tokens=settings.LANGCHAIN_MAX_TOKENS,
    openai_api_key=settings.OPENAI_API_KEY,
)


def get_product_validity_wrt_request(user_query: str, products: list) -> list:
    parser = PydanticOutputParser(pydantic_object=ProductValidationOutputModel)

    prompt = PromptTemplate(
        template=(
            "You are a highly accurate product validation assistant. "
            "Your task is to verify whether the given product exactly matches the user's intent.\n\n"
            "User search query:\n'{query}'\n\n"
            "Product listing:\n{product_details}\n\n"
            "Follow these strict validation rules:\n"
            "1. Sometimes the product specified from the user may not include exactly details provided to you in the product name or title. So there are chance that we may say this particular entry does not match user preferences\n"
            "2. Also there maybe be versions related to products hence we need to keep them in mind as well when matching. If the user has asked to the very minute details regarding any product then we should also match to the miinute detail, else we can skip this\n"
            "3. Avoid false positives due to partial matches or similar names.\n"
            "4. Ignore pricing, ratings, or delivery info for the decision.\n"
            "5. Explain clearly if the product is invalid and why.\n\n"
            "{format_instructions}"
        ),
        input_variables=["query", "product_details"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser
    revised_products = []

    for item in products:
        product_str = "\n".join(f"{k}: {v}" for k, v in item.items())
        parsed = chain.invoke(
            {"query": user_query, "product_details": product_str}
        ).dict()
        if parsed["is_valid_product"] is True:
            item["llm_response"] = parsed
            revised_products.append(item)

    return revised_products
