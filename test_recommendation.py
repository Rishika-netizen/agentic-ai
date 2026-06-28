from recommendation_agent import RecommendationAgent

agent = RecommendationAgent()

results = agent.recommend_products(
    customer_id="C001",
    query="comfortable jeans for college",
    budget=7000
)

print("\nRecommendations:\n")

for product in results:

    print(
        f"SKU: {product['sku']}"
    )

    print(
        f"Name: {product['name']}"
    )

    print(
        f"Price: ₹{product['price_inr']}"
    )

    print(
        f"Stock: {product['stock']}"
    )

    print(
        f"Reason: {product['reason']}"
    )

    print("-" * 50)