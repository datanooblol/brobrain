import requests
from pydantic import BaseModel

class ModelResponse(BaseModel):
    model:str
    role:str
    content:str

class OllamaLlama:
    base_url = "http://localhost:11434/api"
    def __init__(self, model):
        self.model = model
    def OutputMessage(self, response):
        message = response["message"]
        return ModelResponse(
            model=response["model"],
            role=message["role"],
            content=message["content"]
        )
    def run(self, system_prompt, messages)->ModelResponse:
        system_message = {"role": "system", "content": system_prompt}
        response = requests.post(
            f"{self.base_url}/chat",
            json={"model": self.model, "messages": [system_message]+messages, "stream": False},
        )
        return self.OutputMessage(response.json())