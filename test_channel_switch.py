from sales_agent import SalesAgent

agent = SalesAgent()

print("\n===== INSTAGRAM =====\n")


result1 = agent.recommend_for_customer(
    customer_id="C001",
    query="comfortable jeans for college",
    budget=7000,
    channel="Instagram"
)

result2 = agent.recommend_for_customer(
    customer_id="C001",
    query="comfortable jeans for college",
    budget=7000,
    channel="WhatsApp"
)
