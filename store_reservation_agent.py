import os
from dotenv import load_dotenv
from groq import Groq
from agent_logger import log_agent_action

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class StoreReservationAgent:

    def reserve_product(
            self,
            customer_id,
            sku
    ):
        confirmation = self.generate_confirmation(
            customer_id,
            sku
        )

        reservation = {
            "customer_id": customer_id,
            "sku": sku,
            "status": "reserved",
            "store": "Indore Store",
            "pickup_window": "24 hours",
            "confirmation_message": confirmation
        }

        log_agent_action(
            customer_id,
            "StoreReservationAgent",
            f"Reserved SKU {sku} for {customer_id}"
        )

        return reservation

    def generate_confirmation(
            self,
            customer_id,
            sku
    ):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{
                    "role": "user",
                    "content": f"""You are a retail store assistant.
A customer has reserved product {sku} for pickup at our Indore store.
Write one warm, friendly confirmation message telling them:
- Their item is reserved
- They have 24 hours to pick it up
- They can bring this confirmation to the store
Keep it under 2 sentences. No emojis."""
                }],
                max_tokens=80
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return f"Your item {sku} has been reserved at Indore Store. Please collect within 24 hours."