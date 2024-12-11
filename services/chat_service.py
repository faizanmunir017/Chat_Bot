from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

class ChatService:
    def __init__(self, api_key: str, vector_store: InMemoryVectorStore):
        self.client = OpenAI(api_key=api_key)
        self.vector_store = vector_store 

    async def chat_with_gpt(self, prompt: str) -> str:
        try:
            docs = self.vector_store.similarity_search(prompt, k=2)  
           
            context = "\n".join([doc.page_content for doc in docs])
            
            full_prompt = f"Here is some context:\n{context}\n\nUser's query: {prompt}"

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  
                messages=[
                    {"role": "system", "content": "You are a helpful assistant.Dont make any information up.If theres a question asked about Mergestack , you should use the context provided to you only. Dont use any information or General thing. Always consult the context provided to you."},
                    {"role": "user", "content": full_prompt},
                ],
            )
            print("Response received: ", response)
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            print("Service error")
            raise Exception(f"OpenAI API error: {e}")
