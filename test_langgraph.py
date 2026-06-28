from langgraph_sales_agent import (
    sales_graph
)

result = sales_graph.invoke(
    {
        "customer_id": "C001",
        "query": "casual jeans",
        "budget": 5000
    }
)

print(result)