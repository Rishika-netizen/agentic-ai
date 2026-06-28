import pandas as pd
from preference_layer import get_preferences
from inventory_agent import InventoryAgent
from semantic_search import semantic_search
from agent_logger import log_agent_action



class RecommendationAgent:

    def __init__(self):

        self.products = pd.read_csv(
            "data/products.csv"
        )

        self.products["price_inr"] = (
            self.products["price"] * 85
        ).round()

        self.inventory_agent = InventoryAgent()

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

        results = semantic_search(
            query,
            top_k=20
        )

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
            stock_info = (
                self.inventory_agent
                .check_stock(
                    customer_id,
                    sku
                )
            )

            if not stock_info["available"]:
                continue

            recommendations.append(
                {
                    "sku": sku,
                    "name": row["name"],
                    "price_inr": row["price_inr"],
                    "stock": stock_info["stock"],
                    "reason":
    f"Matches your {style} style preference and is currently available in stock"
                }

            )
            log_agent_action(
                customer_id,
                "RecommendationAgent",
                "Generated recommendations"
            )
            return recommendations[:5]