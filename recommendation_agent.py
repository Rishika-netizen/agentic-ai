import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preference_layer import get_preferences
from inventory_agent import InventoryAgent
from semantic_search import semantic_search
from agent_logger import log_agent_action

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class RecommendationAgent:

    def __init__(self):
        self.products = pd.read_csv(
            "data/products.csv"
        )
        self.products["price_inr"] = (
            self.products["price"] * 95
        ).round()

        self.inventory_agent = InventoryAgent()


        self.product_texts = [
            str(row["name"]) + " " +
            str(row["description"]) + " " +
            str(row["terms"])
            for _, row in self.products.iterrows()
        ]

        self.tfidf = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        self.tfidf_matrix = (
            self.tfidf.fit_transform(
                self.product_texts
            )
        )

    def tfidf_search(
            self,
            query,
            top_k=20
    ):
        query_vec = self.tfidf.transform(
            [query]
        )

        similarities = cosine_similarity(
            query_vec,
            self.tfidf_matrix
        )[0]

        top_indices = (
            similarities.argsort()
            [-top_k:][::-1]
        )

        results = []
        for idx in top_indices:
            results.append(
                self.products.iloc[idx]
            )

        return results

    def generate_reason(
            self,
            product_name,
            style,
            query
    ):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{
                    "role": "user",
                    "content": f"""You are a helpful fashion assistant 
    in an Indian retail store.
    In one short sentence, explain why '{product_name}' 
    is a good recommendation for someone looking 
    for '{query}' with {style} style.
    Be specific, natural and friendly. 
    Do not start with 'I'."""
                }],
                max_tokens=60
            )
            return (
                response.choices[0]
                .message.content.strip()
            )
        except Exception as e:
            print(f"GROQ ERROR: {e}")  # ADD THIS LINE
            return (
                f"Matches your {style} style "
                f"preference and is currently "
                f"available in stock"
            )

    def recommend_products(
            self,
            customer_id,
            query,
            budget,
            style
    ):
        preferences = get_preferences(
            customer_id
        )
        disliked_products = (
            preferences["disliked_products"]
        )


        semantic_results = semantic_search(
            query,
            top_k=20
        )


        tfidf_results = self.tfidf_search(
            query,
            top_k=20
        )


        seen_skus = set()
        combined = []

        for row in semantic_results + tfidf_results:
            sku = str(row["sku"])
            if sku not in seen_skus:
                seen_skus.add(sku)
                combined.append(row)

        recommendations = []

        for row in combined:
            sku = row["sku"]


            if row["price_inr"] > budget:
                continue


            if sku in disliked_products:
                continue


            stock_info = (
                self.inventory_agent.check_stock(
                    customer_id,
                    sku
                )
            )
            if not stock_info["available"]:
                continue


            reason = self.generate_reason(
                row["name"],
                style,
                query
            )

            recommendations.append({
                "sku": sku,
                "name": row["name"],
                "price_inr": float(
                    row["price_inr"]
                ),
                "stock": stock_info["stock"],
                "reason": reason
            })

        log_agent_action(
            customer_id,
            "RecommendationAgent",
            f"Generated {len(recommendations)} "
            f"recommendations using hybrid "
            f"TF-IDF + semantic search"
        )

        return recommendations[:5]