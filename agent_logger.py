import json
from datetime import datetime


def log_agent_action(
    customer_id,
    agent_name,
    action
):
    try:
        with open(
            "data/agent_logs.json",
            "r"
        ) as f:
            logs = json.load(f)

    except:
        logs = []

    logs.append(
        {
            "timestamp": str(datetime.now()),
            "customer_id": customer_id,
            "agent": agent_name,
            "action": action
        }
    )

    with open(
        "data/agent_logs.json",
        "w"
    ) as f:
        json.dump(
            logs,
            f,
            indent=4
        )