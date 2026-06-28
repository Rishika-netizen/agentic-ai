from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)


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

        self.style_embeddings = (
            self.model.encode(
                list(
                    self.styles.values()
                )
            )
        )

    def detect_style(
            self,
            query
    ):

        query_embedding = (
            self.model.encode(
                [query]
            )
        )

        similarities = (
            cosine_similarity(
                query_embedding,
                self.style_embeddings
            )[0]
        )

        best_index = (
            similarities.argmax()
        )

        style = list(
            self.styles.keys()
        )[best_index]

        return style