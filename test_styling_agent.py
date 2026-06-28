from styling_agent import StylingAgent

agent = StylingAgent()

print(
    agent.detect_style(
        "comfortable clothes for college"
    )
)

print(
    agent.detect_style(
        "shirt for job interview"
    )
)

print(
    agent.detect_style(
        "outfit for birthday party"
    )
)

print(
    agent.detect_style(
        "clothes for gym"
    )
)