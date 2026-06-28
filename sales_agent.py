from journey_intelligence import build_profile
from recommendation_agent import RecommendationAgent
from inventory_agent import InventoryAgent
from payment_agent import PaymentAgent
from session_manager import SessionManager
from store_reservation_agent import (
    StoreReservationAgent
)
from styling_agent import StylingAgent
from agent_logger import log_agent_action
from followup_agent import FollowUpAgent
from human_support_agent import (
    HumanSupportAgent
)

class SalesAgent:

    def __init__(self):

        self.recommendation_agent = (
            RecommendationAgent()
        )

        self.inventory_agent = (
            InventoryAgent()
        )

        self.payment_agent = (
            PaymentAgent()
        )

        self.session_manager = (
            SessionManager()
        )

        self.store_agent = (
            StoreReservationAgent()
        )
        self.styling_agent = StylingAgent()

        self.followup_agent = (
            FollowUpAgent()
        )
        self.human_support_agent = (
            HumanSupportAgent()
        )


    def recommend_for_customer(
            self,
            customer_id,
            query,
            budget,
            channel
    ):
        self.session_manager.update_channel(
            customer_id,
            channel
        )

        profile = build_profile(
            customer_id
        )

        favorite_products = (
            profile["favorite_products"]
        )

        style = self.styling_agent.detect_style(query)
        log_agent_action(customer_id, "StylingAgent", f"Detected style: {style}")

        if not favorite_products:
            log_agent_action(
                customer_id, "SalesAgent",
                "No history found, falling back to query-only recommendation"
            )
            enhanced_query = query
        else:
            enhanced_query = style + " " + query

        recommendations = self.recommendation_agent.recommend_products(
            customer_id, enhanced_query, budget, style

        )
        self.session_manager.save_recommendations(
            customer_id,
            recommendations
        )

        return {
            "customer_id": customer_id,
            "detected_style": style,
            "purchase_intent": profile["purchase_intent"],
            "preferred_channel": profile["preferred_channel"],
            "current_channel": channel,
            "query": query,
            "recommendations": recommendations
        }

    def check_inventory(
            self,
            customer_id,
            sku
    ):

        stock_info = (
            self.inventory_agent
            .check_stock(
                customer_id,
                sku
            )
        )

        return stock_info

    def purchase_product(
            self,
            customer_id,
            amount
    ):

        payment_result = (
            self.payment_agent
            .process_payment(
                customer_id,
                amount
            )
        )

        self.session_manager.save_payment_status(
            customer_id,
            payment_result
        )

        if payment_result["status"] != "success":
            escalation = (
                self.escalate_to_human(
                    customer_id,
                    payment_result["status"]
                )
            )

            return {
                "customer_id": customer_id,
                "payment_status":
                    payment_result["status"],

                "message":
                    "Payment failed",

                "recovery":
                    payment_result["recovery"],

                "escalation":
                    escalation
            }
        return {
            "customer_id": customer_id,
            "payment_status": "success",
            "message":
                "Payment completed successfully"
        }

    def reserve_product(
            self,
            customer_id,
            sku
    ):

        return (
            self.store_agent
            .reserve_product(
                customer_id,
                sku
            )
        )

    def send_followup(
            self,
            customer_id
    ):

        return (
            self.followup_agent
            .send_followup(
                customer_id
            )
        )

    def escalate_to_human(
            self,
            customer_id,
            issue
    ):

        return (
            self.human_support_agent
            .escalate(
                customer_id,
                issue
            )
        )


    def switch_channel(self, customer_id, new_channel):
        prev = self.session_manager.get_channel(customer_id)
        self.session_manager.update_channel(customer_id, new_channel)
        log_agent_action(
            customer_id, "SalesAgent",
            f"Channel switch: {prev} → {new_channel}"
        )
        return {
            "previous_channel": prev,
            "current_channel": new_channel,
            "context_preserved": True
        }
if __name__ == "__main__":
        agent = SalesAgent()

        print(
            agent.recommend_for_customer(
                "C001",
                "comfortable clothes for college",
                5000,
                "Instagram"
            )
        )



