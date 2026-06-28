import json


def get_preferences(customer_id):

    with open(
        "data/journey_events.json",
        "r"
    ) as f:
        events = json.load(f)

    liked = []
    disliked = []
    reasons = []

    for event in events:

        if event["customer_id"] != customer_id:
            continue

        if event["event_type"] == "purchase":
            liked.append(
                event["sku"]
            )

        if event["event_type"] == "dislike":

            disliked.append(
                event["sku"]
            )

            reasons.append(
                event.get(
                    "reason",
                    ""
                )
            )

    return {
        "liked_products": liked,
        "disliked_products": disliked,
        "dislike_reasons": reasons
    }