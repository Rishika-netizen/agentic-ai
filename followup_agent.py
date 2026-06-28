from agent_logger import log_agent_action
from session_manager import SessionManager

class FollowUpAgent:
    def __init__(self):
        self.session_manager = SessionManager()

    def send_followup(self, customer_id):
        session = self.session_manager.get_session(customer_id)


        last_payment = session.get("last_payment", {})
        if last_payment.get("status") != "success":
            return {
                "customer_id": customer_id,
                "channel": session.get("current_channel"),
                "message": "We noticed your payment didn't go through. Need help completing your purchase?"
            }

        return {
            "customer_id": customer_id,
            "channel": session.get("current_channel"),
            "message": "Hope you're enjoying your purchase! Here are some matching products."
        }
        log_agent_action(
            customer_id,
            "FollowUpAgent",
            "Sent follow-up message"
        )

        return response