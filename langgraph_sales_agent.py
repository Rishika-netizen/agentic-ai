from typing import TypedDict
from langgraph.graph import (
    StateGraph,
    START,
    END
)
from styling_agent import StylingAgent
from recommendation_agent import RecommendationAgent
from inventory_agent import InventoryAgent
from payment_agent import PaymentAgent
from human_support_agent import HumanSupportAgent
from session_manager import SessionManager
from agent_logger import log_agent_action

# ----------------------------
# Agent Objects
# ----------------------------
styling_agent = StylingAgent()
recommendation_agent = RecommendationAgent()
inventory_agent = InventoryAgent()
payment_agent = PaymentAgent()
human_support_agent = HumanSupportAgent()
session_manager = SessionManager()

# ----------------------------
# Shared State
# ----------------------------
class SalesState(TypedDict):
    customer_id: str
    query: str
    budget: int
    channel: str
    style: str
    recommendations: list
    inventory_status: dict
    payment_result: dict
    escalation: dict
    error: str

# ----------------------------
# Styling Node
# ----------------------------
def styling_node(state):
    style = styling_agent.detect_style(
        state["query"]
    )
    log_agent_action(
        state["customer_id"],
        "StylingAgent",
        f"Detected style: {style}"
    )
    return {"style": style}

# ----------------------------
# Recommendation Node
# ----------------------------
def recommendation_node(state):
    recommendations = (
        recommendation_agent.recommend_products(
            state["customer_id"],
            state["query"],
            state["budget"],
            state["style"]
        )
    )
    session_manager.save_recommendations(
        state["customer_id"],
        recommendations
    )
    log_agent_action(
        state["customer_id"],
        "RecommendationAgent",
        f"Found {len(recommendations)} recommendations"
    )
    return {"recommendations": recommendations}

# ----------------------------
# Inventory Node
# ----------------------------
def inventory_node(state):
    inventory_results = {}
    for product in state["recommendations"]:
        sku = product["sku"]
        inventory_results[sku] = (
            inventory_agent.check_stock(
                state["customer_id"],
                sku
            )
        )
    log_agent_action(
        state["customer_id"],
        "InventoryAgent",
        f"Checked stock for {len(inventory_results)} products"
    )
    return {"inventory_status": inventory_results}

# ----------------------------
# Payment Node
# ----------------------------
def payment_node(state):
    payment_result = payment_agent.process_payment(
        state["customer_id"],
        state["budget"]
    )
    session_manager.save_payment_status(
        state["customer_id"],
        payment_result
    )
    log_agent_action(
        state["customer_id"],
        "PaymentAgent",
        f"Payment status: {payment_result['status']}"
    )
    return {"payment_result": payment_result}

# ----------------------------
# Human Support Node
# ----------------------------
def human_support_node(state):
    escalation = human_support_agent.escalate(
        state["customer_id"],
        state["payment_result"]["status"]
    )
    log_agent_action(
        state["customer_id"],
        "HumanSupportAgent",
        f"Escalated issue: {state['payment_result']['status']}"
    )
    return {"escalation": escalation}

# ----------------------------
# Conditional Routing
# ----------------------------
def payment_router(state):
    if state["payment_result"]["status"] == "success":
        return "success"
    return "failure"

# ----------------------------
# Graph
# ----------------------------
graph = StateGraph(SalesState)

graph.add_node("styling", styling_node)
graph.add_node("recommendation", recommendation_node)
graph.add_node("inventory", inventory_node)
graph.add_node("payment", payment_node)
graph.add_node("human_support", human_support_node)

# ----------------------------
# Edges
# ----------------------------
graph.add_edge(START, "styling")
graph.add_edge("styling", "recommendation")
graph.add_edge("recommendation", "inventory")
graph.add_edge("inventory", "payment")
graph.add_conditional_edges(
    "payment",
    payment_router,
    {
        "success": END,
        "failure": "human_support"
    }
)
graph.add_edge("human_support", END)

# ----------------------------
# Compile
# ----------------------------
sales_graph = graph.compile()

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    print("\n===== LANGGRAPH JOURNEY =====\n")

    result = sales_graph.invoke({
        "customer_id": "C002",
        "query": "casual jeans",
        "budget": 5000,
        "channel": "In-Store Kiosk",
        "style": "",
        "recommendations": [],
        "inventory_status": {},
        "payment_result": {},
        "escalation": {},
        "error": ""
    })

    print("\n--- STYLE DETECTED ---")
    print(result["style"])

    print("\n--- RECOMMENDATIONS ---")
    for r in result["recommendations"]:
        print(r)

    print("\n--- INVENTORY STATUS ---")
    print(result["inventory_status"])

    print("\n--- PAYMENT RESULT ---")
    print(result["payment_result"])

    if result["escalation"]:
        print("\n--- ESCALATION ---")
        print(result["escalation"])

    print("\n===== JOURNEY COMPLETE =====\n")

from IPython.display import Image
graph_image = sales_graph.get_graph().draw_mermaid_png()
with open("agent_graph.png", "wb") as f:
    f.write(graph_image)