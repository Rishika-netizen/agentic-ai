import os
from dotenv import load_dotenv
from groq import Groq
from agent_logger import log_agent_action
from session_manager import SessionManager

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class FollowUpAgent:

    def __init__(self):
        self.session_manager = SessionManager()

    def generate_message(
            self,
            customer_id,
            channel,
            payment_success,
            purchased_items
    ):
        try:
            context = (
                f"purchased items: {purchased_items}"
                if payment_success
                else "payment failed"
            )
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{
                    "role": "user",
                    "content": f"""You are a friendly retail assistant sending a follow-up message 
to customer {customer_id} via {channel}.
Context: {context}
Write one short, warm, personalized follow-up message.
If payment failed, help them complete purchase.
If payment succeeded, thank them and suggest they explore more.
Do not use emojis. Keep it under 2 sentences."""
                }],
                max_tokens=80
            )
            return response.choices[0].message.content.strip()
        except Exception:
            if payment_success:
                return "Hope you're enjoying your purchase! Feel free to explore more products."
            return "We noticed your payment didn't go through. Need help completing your purchase?"

    def send_followup(self, customer_id):
        session = self.session_manager.get_session(
            customer_id
        )

        channel = session.get(
            "current_channel",
            "Mobile App"
        )
        last_payment = session.get(
            "last_payment", {}
        )
        payment_success = (
            last_payment.get("status") == "success"
        )
        purchased_items = session.get(
            "recommended_skus", []
        )

        message = self.generate_message(
            customer_id,
            channel,
            payment_success,
            purchased_items
        )

        log_agent_action(
            customer_id,
            "FollowUpAgent",
            f"Sent follow-up via {channel} — payment success: {payment_success}"
        )

        return {
            "customer_id": customer_id,
            "channel": channel,
            "payment_success": payment_success,
            "message": message
        }