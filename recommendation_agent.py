import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq
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

    def generate_reason(
            self,
            product_name,
            style,
            query
    ):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{
                    "role": "user",
                    "content": f"""You are a helpful fashion assistant in an Indian retail store.
In one short sentence, explain why '{product_name}' is a good recommendation
for someone looking for '{query}' with {style} style.
Be specific, natural and friendly. Do not start with 'I'."""
                }],
                max_tokens=60
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return f"Matches your {style} style preference and is currently available in stock"

    def recommend_products(
            self,
            customer_id,
            query,
            budget,
            style
    ):
        preferences = get_preferences(customer_id)
        disliked_products = preferences["disliked_products"]

        results = semantic_search(query, top_k=20)

        recommendations = []

        for row in results:
            sku = row["sku"]

            # Budget filter
            if row["price_inr"] > budget:
                continue

            # Preference filter
            if sku in disliked_products:
                continue

            # Inventory check
            stock_info = self.inventory_agent.check_stock(
                customer_id,
                sku
            )
            if not stock_info["available"]:
                continue

            # LLM generated reason
            reason = self.generate_reason(
                row["name"],
                style,
                query
            )

            recommendations.append({
                "sku": sku,
                "name": row["name"],
                "price_inr": float(row["price_inr"]),
                "stock": stock_info["stock"],
                "reason": reason
            })

        # fixed - moved outside loop
        log_agent_action(
            customer_id,
            "RecommendationAgent",
            f"Generated {len(recommendations)} recommendations"
        )
        return recommendations[:5]