from agent_logger import log_agent_action


class HumanSupportAgent:

    def escalate(
            self,
            customer_id,
            issue
    ):

        log_agent_action(
            customer_id,
            "HumanSupportAgent",
            f"Escalated issue: {issue}"
        )

        return {
            "customer_id": customer_id,
            "status": "escalated",
            "message":
                "Connecting you with a human support representative",
            "issue": issue
        }