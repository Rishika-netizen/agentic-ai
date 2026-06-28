from sales_agent import SalesAgent

agent = SalesAgent()

print(
    "\n===== STEP 1 : KIOSK =====\n"
)

result = (
    agent.recommend_for_customer(
        customer_id="C002",
        query="casual jeans",
        budget=5000,
        channel="In-Store Kiosk"
    )
)

print(result)

print(
    "\n===== STEP 2 : PURCHASE =====\n"
)

payment = (
    agent.purchase_product(
        "C002",
        4000
    )
)

print(payment)

print("\n===== CHANNEL SWITCH =====\n")
switch = agent.switch_channel("C002", "Mobile App")
print(switch)

print("\n===== STEP 3 : MOBILE APP FOLLOW-UP =====\n")
followup = agent.send_followup("C002")
print(followup)




