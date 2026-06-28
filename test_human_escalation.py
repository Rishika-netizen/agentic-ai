from sales_agent import SalesAgent

agent = SalesAgent()

for i in range(5):

    print(
        agent.purchase_product(
            "C001",
            5000
        )
    )