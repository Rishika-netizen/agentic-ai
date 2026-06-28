import os
from dotenv import load_dotenv
from groq import Groq
from agent_logger import log_agent_action

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class HumanSupportAgent:

    def escalate(
            self,
            customer_id,
            issue
    ):
        message = self.generate_message(
            customer_id,
            issue
        )

        log_agent_action(
            customer_id,
            "HumanSupportAgent",
            f"Escalated issue: {issue}"
        )

        return {
            "customer_id": customer_id,
            "status": "escalated",
            "issue": issue,
            "message": message
        }

    def generate_message(
            self,
            customer_id,
            issue
    ):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{
                    "role": "user",
                    "content": f"""You are a retail customer support assistant.
A customer has faced this issue: {issue}
Write one short, empathetic message telling them a human representative 
will help them resolve this specific issue.
Be specific to the issue, warm and professional.
Do not use emojis. Max 2 sentences."""
                }],
                max_tokens=80
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return "Connecting you with a human support representative who will resolve your issue shortly."