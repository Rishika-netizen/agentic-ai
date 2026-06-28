from sales_agent import SalesAgent

agent = SalesAgent()

print("\n===== STEP 1 : INSTAGRAM =====\n")

result = agent.recommend_for_customer(
    customer_id="C001",
    query="comfortable jeans for college",
    budget=7000,
    channel="Instagram"
)

print(result)

recommendations = result["recommendations"]

if not recommendations:

    print("No recommendations found")
    exit()

sku = recommendations[0]["sku"]

print("\nSelected SKU:", sku)

print("\n===== INVENTORY CHECK =====\n")

inventory = agent.check_inventory(
    "C001",
    sku
)

print(inventory)

print("\n===== PAYMENT =====\n")

payment = agent.purchase_product(
    "C001",
    5000
)

print(payment)

if payment["payment_status"] != "success":

    print("\nSwitching to WhatsApp...\n")

    resumed = (
        agent.recommend_for_customer(
            customer_id="C001",
            query="comfortable jeans for college",
            budget=7000,
            channel="WhatsApp"
        )
    )

    print(resumed)