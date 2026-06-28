from agent_logger import log_agent_action


class StoreReservationAgent:

    def reserve_product(
            self,
            customer_id,
            sku
    ):

        reservation = {
            "customer_id": customer_id,
            "sku": sku,
            "status": "reserved",
            "store": "Indore Store",
            "pickup_window": "24 hours"
        }

        log_agent_action(
            customer_id,
            "StoreReservationAgent",
            f"Reserved {sku}"
        )

        return reservation