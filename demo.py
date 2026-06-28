from sales_agent import SalesAgent

agent = SalesAgent()

result = agent.recommend_for_customer(
    "C001",
    7000
)

print(result)