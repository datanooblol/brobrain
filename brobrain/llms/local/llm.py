import requests
from abc import ABC, abstractmethod
import time
from brobrain.models.conversation import Conversation

class BaseOllama(ABC):
    base_url = "http://localhost:11434/api"
    def __init__(self, model:str):
        self.model = model

    @abstractmethod
    def OutputMessage(self, response:dict, executed_time_ms:float) -> Conversation: return

    def run(self, system_prompt, messages)->Conversation:
        system_message = {"role": "system", "content": system_prompt}
        start = time.perf_counter()
        response = requests.post(
            f"{self.base_url}/chat",
            json={"model": self.model, "messages": [system_message]+messages, "stream": False},
        )
        end = time.perf_counter()
        executed_time_ms = elapsed_ms = (end - start) * 1000
        return self.OutputMessage(response.json(), executed_time_ms)
            
class OllamaLlama(BaseOllama):
    def __init__(self, model:str):
        super().__init__(model=model)

    def OutputMessage(self, response:dict, executed_time_ms:float) -> Conversation:
        message = response["message"]
        return Conversation(
            model=response["model"],
            role=message["role"],
            content=message["content"],
            executed_time_ms=executed_time_ms
        )
    
class OllamaOpenAI(BaseOllama):
    def __init__(self, model):
        super().__init__(model=model)

    def OutputMessage(self, response:dict, execute_time_ms:float) -> Conversation:
        message = response["message"]
        return Conversation(
            model=response["model"],
            role=message["role"],
            content=message["content"],
            reason=message["thinking"],
            executed_time_ms=execute_time_ms
        )