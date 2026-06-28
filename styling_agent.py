import os
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from agent_logger import log_agent_action

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class StylingAgent:

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )
        self.styles = {
            "casual":
                "college wear casual everyday clothing jeans tshirts",
            "formal":
                "office interview business professional formal clothing",
            "partywear":
                "party wedding festive stylish fashion outfits",
            "sportswear":
                "gym running workout athletic sports clothing"
        }
        self.style_embeddings = self.model.encode(
            list(self.styles.values())
        )

    def detect_style(self, query):


        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(
            query_embedding,
            self.style_embeddings
        )[0]
        best_index = similarities.argmax()
        confidence = similarities[best_index]
        style = list(self.styles.keys())[best_index]


        if confidence < 0.3:
            style = self.llm_detect_style(query)

        log_agent_action(
            "system",
            "StylingAgent",
            f"Detected style: {style} (confidence: {confidence:.2f})"
        )

        return style

    def llm_detect_style(self, query):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{
                    "role": "user",
                    "content": f"""Classify this shopping query into exactly one category:
casual, formal, partywear, sportswear.
Query: {query}
Reply with just the single word, nothing else."""
                }],
                max_tokens=10
            )
            result = response.choices[0].message.content.strip().lower()
            if result in self.styles:
                return result
            return "casual"
        except Exception:
            return "casual"