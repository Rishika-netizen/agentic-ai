import os

os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer

products = pd.read_csv("data/products.csv")
products["price_inr"] = (
        products["price"] * 95
).round()

model = SentenceTransformer("all-MiniLM-L6-v2")


chroma_client = chromadb.PersistentClient(
    path="data/vectordb"
)

collection = chroma_client.get_or_create_collection(
    name="products"
)

if collection.count() == 0:
    print("Indexing products into vector DB...")

    product_texts = []
    skus = []
    seen = set()  # ADD THIS

    for _, row in products.iterrows():
        sku = str(row["sku"])

        if sku in seen:  # ADD THIS
            continue  # skip duplicates
        seen.add(sku)  # ADD THIS

        text = (
                str(row["name"]) + " " +
                str(row["description"]) + " " +
                str(row["terms"])
        )
        product_texts.append(text)
        skus.append(sku)

    embeddings = model.encode(
        product_texts
    ).tolist()

    collection.add(
        documents=product_texts,
        embeddings=embeddings,
        ids=skus
    )
    print(f"Indexed {len(skus)} products")


def semantic_search(query, top_k=20):
    query_embedding = model.encode(
        [query]
    ).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    matched_skus = results["ids"][0]

    output = []
    for sku in matched_skus:
        row = products[
            products["sku"].astype(str) == sku
            ]
        if not row.empty:
            output.append(row.iloc[0])

    return output