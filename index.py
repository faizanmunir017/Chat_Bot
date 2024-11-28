# Embedding API Testing : 


from dotenv import load_dotenv
from openai import OpenAI

print("Embedding API : ")

load_dotenv()
client = OpenAI()


response = client.embeddings.create(
    input="Your text string goes here",
    model="text-embedding-3-small"
)

print(response.data[0].embedding)