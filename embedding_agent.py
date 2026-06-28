import pandas as pd
from sentence_transformers import SentenceTransformer

# Load products
products = pd.read_csv("data/products.csv")

# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Create text for each product
product_texts = []

for _, row in products.iterrows():

    text = (
        str(row["name"]) + " " +
        str(row["description"]) + " " +
        str(row["terms"])
    )

    product_texts.append(text)

# Generate embeddings
embeddings = model.encode(
    product_texts,
    show_progress_bar=True
)

print("Total embeddings:", len(embeddings))
print("Embedding dimension:", len(embeddings[0]))