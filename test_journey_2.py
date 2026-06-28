from sales_agent import SalesAgent

agent = SalesAgent()

print(
    "\n===== STEP 1 : WHATSAPP =====\n"
)

result = (
    agent.recommend_for_customer(
        customer_id="C003",
        query="comfortable clothes for college",
        budget=5000,
        channel="WhatsApp"
    )
)

print(result)

recommendations = (
    result["recommendations"]
)

sku = (
    recommendations[0]["sku"]
)

print(
    "\nSelected SKU:",
    sku
)

print(
    "\n===== STEP 2 : INVENTORY =====\n"
)

inventory = (
    agent.check_inventory(
        "C003",
        sku
    )
)

print(inventory)

print(
    "\n===== STEP 3 : RESERVE IN STORE =====\n"
)

reservation = (
    agent.reserve_product(
        "C003",
        sku
    )
)

print(reservation)

print(
    "\n===== STEP 4 : STORE VISIT =====\n"
)

print(
    "Customer visits store and tries product"
)
print(
    "\n===== STEP 5 : PURCHASE =====\n"
)

payment = (
    agent.purchase_product(
        "C003",
        4000
    )
)

print(payment)