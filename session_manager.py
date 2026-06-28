import json
import datetime


class SessionManager:

    def __init__(self):
        self.file_path = "data/sessions.json"

    def get_session(self, customer_id):
        try:
            with open(self.file_path, "r") as f:
                sessions = json.load(f)
        except FileNotFoundError:
            sessions = {}

        return sessions.get(customer_id, {})

    def save_session(self, customer_id, session_data):
        try:
            with open(self.file_path, "r") as f:
                sessions = json.load(f)
        except FileNotFoundError:
            sessions = {}

        sessions[customer_id] = session_data

        with open(self.file_path, "w") as f:
            json.dump(
                sessions,
                f,
                indent=4
            )
        session_data["last_updated"] = datetime.datetime.now().isoformat()
        sessions[customer_id] = session_data
        with open(self.file_path, "w") as f:
            json.dump(sessions, f, indent=4)

    def update_channel(self, customer_id, channel):
        session = self.get_session(customer_id)

        session["current_channel"] = channel

        self.save_session(
            customer_id,
            session
        )
        if "current_channel" in session:
            session["previous_channel"] = session["current_channel"]
        session["current_channel"] = channel
        self.save_session(customer_id, session)

    def get_channel(self, customer_id):
        session = self.get_session(customer_id)
        return session.get("current_channel", "Unknown")

    def save_recommendations(self, customer_id, recommendations):
        session = self.get_session(customer_id)

        session["recommended_skus"] = [
            product["sku"]
            for product in recommendations
        ]

        self.save_session(
            customer_id,
            session
        )

    def save_payment_status(self, customer_id, payment_result):
        session = self.get_session(customer_id)

        session["last_payment"] = payment_result

        self.save_session(
            customer_id,
            session
        )