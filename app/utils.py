from sentence_transformers import SentenceTransformer  # type: ignore
from app.logger import app_logger as logging
from app.config import settings
import numpy as np  # type: ignore

model = SentenceTransformer(settings.SENTENCE_TRANSFORMERS_EMBEDDING_MODEL_NAME)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def filter_by_embedding(query: str, products: list, threshold: float = 0.6) -> list:
    names = [p["product_name"] for p in products]
    embeddings = model.encode([query] + names, convert_to_numpy=True)
    query_emb = embeddings[0]
    product_embs = embeddings[1:]

    filtered = []

    for product, emb in zip(products, product_embs):
        similarity = cosine_similarity(query_emb, emb)
        similarity = min(1.0, max(0.0, similarity))

        if similarity >= threshold:
            product["similarity"] = similarity
            filtered.append(product)

    return sorted(filtered, key=lambda x: (-x["similarity"], float(x["price"])))[:20]
