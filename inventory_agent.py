import json
from agent_logger import log_agent_action


class InventoryAgent:

    def __init__(self):

        with open(
            "data/inventory.json",
            "r"
        ) as f:
            self.inventory = json.load(f)

    def get_inventory_by_sku(
            self,
            sku
    ):

        return self.inventory.get(
            sku,
            None
        )

    def check_stock(
            self,
            customer_id,
            sku
    ):
        if sku not in self.inventory:
            log_agent_action(
                customer_id,
                "InventoryAgent",
                f"Checked stock for {sku}"
            )

            return {
                "available": False,
                "stock": 0
            }

        total_stock = sum(
            self.inventory[sku]["sizes"].values()
        )
        log_agent_action(
            customer_id,
            "InventoryAgent",
            f"Checked stock for {sku}"
        )

        return {
            "available": total_stock > 0,
            "stock": total_stock
        }