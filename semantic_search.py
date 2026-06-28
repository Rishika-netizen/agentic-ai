from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

products = pd.read_csv("data/products.csv")
products["price_inr"] = (
    products["price"] * 85
).round()

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

product_texts = []

for _, row in products.iterrows():

    text = (
        str(row["name"]) + " " +
        str(row["description"]) + " " +
        str(row["terms"])
    )

    product_texts.append(text)

product_embeddings = model.encode(
    product_texts
)


def semantic_search(
        query,
        top_k=20
):

    query_embedding = model.encode(
        [query]
    )

    similarities = cosine_similarity(
        query_embedding,
        product_embeddings
    )[0]

    top_indices = similarities.argsort()[
        -top_k:
    ][::-1]

    results = []

    for idx in top_indices:

        results.append(
            products.iloc[idx]
        )

    return results