import random
from agent_logger import log_agent_action


class PaymentAgent:

    def process_payment(
            self,
            customer_id,
            amount
    ):

        status = random.choice(
            [
                "success",
                "upi_failure",
                "bank_timeout"
            ]
        )

        response = {
            "customer_id": customer_id,
            "amount": amount,
            "status": status
        }

        if status == "upi_failure":

            response["recovery"] = (
                "Try credit/debit card"
            )

        elif status == "bank_timeout":

            response["recovery"] = (
                "Retry after a few minutes"
            )

        log_agent_action(
            customer_id,
            "PaymentAgent",
            f"Payment status: {status}"
        )

        return response