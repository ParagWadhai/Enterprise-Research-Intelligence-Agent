from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingService:

    def __init__(self):

        self.model = SentenceTransformer(
            MODEL_NAME
        )

    def embed(
        self,
        texts: list[str],
    ):

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

    def embed_query(
        self,
        query: str,
    ):

        return self.model.encode(
            [query],
            normalize_embeddings=True,
            show_progress_bar=False,
        )


embedding_service = EmbeddingService()