from brobrain.llms.local.embedding import OllamaEmbedding
from brobrain.llms.local.llm import OllamaLlama
from brobrain.models.conversation import Conversation, RoleType
from brobrain.models.episode import Episode
from brobrain.memories.conversation import DuckConversation
from brobrain.memories.episode import DuckEpisode
from typing import List

SESSION_ID = "test"
# MODEL_NAME = "mrasif/llama3.2:1b"
MODEL_NAME = "gpt-oss:20b"
EMBEDDING_NAME = "bge-m3"

system_prompt = "You are Andy who're always chill and supportive. Always answer in bro-like manner. Always answer in short like human does."
episode_system_prompt = "Use USER_INPUT and ASSISTANT_INPUT and summarize them as clear and concise as possible. Do not summarize off topics."
def UserMessage(content:str)->dict:
    return {"role": RoleType.USER, "content": content}

def main():
    embedder = OllamaEmbedding(model=EMBEDDING_NAME)
    vector_size = len(embedder.run("test").embeddings[0])
    llm = OllamaLlama(model=MODEL_NAME)
    dc = DuckConversation()
    de = DuckEpisode(vector_size=vector_size)
    while True:
        user_input = input("User: ")
        if user_input == "exit":
            break
        content = user_input
        user_convo = Conversation(model=MODEL_NAME, content=user_input, session_id=SESSION_ID)
        chat_history = dc.read(session_id=SESSION_ID, order_asc=True, limit=6)
        if len(chat_history)>0:
            chat_history = [{"role":ch.role, "content":ch.content} for ch in chat_history]
            # print(len(chat_history))
        episode_history = de.vector_search(embedder.run(user_input).embeddings[0], limit=5)
        if episode_history:
            episode_history = "\n".join([ep.content for ep in episode_history])
            content = f"PREVIOUS:\n\n{episode_history}\n\nUSER_INPUT:\n\n{user_input}"
        ai_convo = llm.run(system_prompt, messages=chat_history+[UserMessage(content)])
        print("AI:", ai_convo.content)
        ai_convo.session_id = SESSION_ID
        dc.create(user_convo)
        dc.create(ai_convo)
        episode_prompt = f"USER: {user_convo.content}\nASSISTANT: {ai_convo.content}"
        episode_convo = llm.run(episode_system_prompt, messages=[UserMessage(episode_prompt)])
        episode = Episode(
            model=MODEL_NAME,
            content=episode_convo.content,
            conversation_ids=[user_convo.id, ai_convo.id],
            session_id=SESSION_ID,
            vector=embedder.run(episode_convo.content).embeddings[0]
        )
        de.create(episode)

if __name__ == "__main__":
    main()