from inventory_agent import InventoryAgent

agent = InventoryAgent()

print(
    agent.check_stock(
        "C001",
        "326540983-802-36"
    )
)