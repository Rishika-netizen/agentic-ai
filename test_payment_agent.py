from payment_agent import PaymentAgent

agent = PaymentAgent()

print(
    agent.process_payment(
        "C001",
        5000
    )
)