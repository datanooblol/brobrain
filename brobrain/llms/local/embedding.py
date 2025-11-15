import requests
from pydantic import BaseModel

class EmbeddingResponse(BaseModel):
    model:str
    embeddings: list[list[float]]

class OllamaEmbedding:
    base_url = "http://localhost:11434/api"
    def __init__(self, model):
        self.model = model

    def run(self, texts)->EmbeddingResponse:
        if isinstance(texts, str):
            texts = [texts]
        response = requests.post(
            f"{self.base_url}/embed",
            json={"model": self.model, "input": texts},
        )
        return EmbeddingResponse(**response.json())
        # return response.json()