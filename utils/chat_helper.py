
from typing import List
from models.message_schema import Message
from langchain_core.documents import Document
from langchain.chains.summarize import load_summarize_chain

async def store_message(sender: str, text: str, collection):
    message = Message(sender=sender, text=text)
    collection.insert_one(message.model_dump())

async def get_last_messages(collection) -> List[dict]:
    try:
        messages = list(collection.find().sort("_id", -1).limit(10)) 
        messages.reverse()
        messages_list = [{"sender": message["sender"], "text": message["text"]} for message in messages]
        return messages_list
    except Exception as e:
        print(f"Error in getting messages from Db: {e}")

async def summarize_context(context: str, model, max_words: int = 200) -> str:
    docs = [Document(page_content=context)]
    chain = load_summarize_chain(model, chain_type="stuff")
    summary = chain.run(docs)
    print("Summary is: ", summary)
    return summary
