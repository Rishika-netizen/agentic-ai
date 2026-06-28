import pandas as pd
from sentence_transformers import SentenceTransformer


products = pd.read_csv("data/products.csv")


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


embeddings = model.encode(
    product_texts,
    show_progress_bar=True
)

print("Total embeddings:", len(embeddings))
print("Embedding dimension:", len(embeddings[0]))