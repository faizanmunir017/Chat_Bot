from openai import OpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langsmith import traceable
from langchain.schema.retriever import BaseRetriever
from models.message_schema import Message
from pymongo.collection import Collection
from utils.constant import chat_instructions
from typing import List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document


class ChatService:
    def __init__(self, api_key: str, vector_store: InMemoryVectorStore,retriever:BaseRetriever,db_collection:Collection):
        self.model = ChatOpenAI(api_key=api_key,model="gpt-4o-mini", temperature=0.7)
        self.vector_store = vector_store 
        self.retriever=retriever
        self.collection=db_collection
        self.summarizer = LsaSummarizer()
        self.condense_question_prompt = PromptTemplate.from_template(chat_instructions["condense_question_prompt"])
        self.answer_prompt = PromptTemplate.from_template(chat_instructions["answer_prompt"])

    async def store_message(self,sender:str,text:str):
        message=Message(sender=sender,text=text)
        self.collection.insert_one(message.model_dump())

    async def get_last_messages(self)->List[dict]:
        try:
            messages=list(self.collection.find().sort("_id",-1).limit(10)) 
            messages.reverse()
            messages_list = [{"sender": message["sender"], "text": message["text"]} for message in messages]
            return messages_list 

        except Exception as e:
            print( f"Error in getting messages from Db: {e}")


    async def summarize_context(self, context: str, max_words: int = 200) -> str:
        docs = [Document(page_content=context)]
        chain = load_summarize_chain(self.model, chain_type="stuff")
        summary = chain.run(docs)
        print("Summary is : ", summary)
        return summary

    @traceable(project_name="ChatBot_Interactions")
    async def chat_with_gpt(self, prompt: str) -> str:
        try:
            print("In chat with gpt")
            await self.store_message(sender="user", text=prompt)
            docs = await self.retriever.aget_relevant_documents(prompt)
            full_context = "\n".join([doc.page_content for doc in docs])
            context = await self.summarize_context(full_context)

            chat_history = await self.get_last_messages()

            standalone_question_chain = (
                RunnablePassthrough.assign(
                    standalone_question=(
                        self.condense_question_prompt
                        | self.model
                        | StrOutputParser()
                    )
                )
            )

            answer_chain = (
                RunnablePassthrough.assign(
                    response=(
                        self.answer_prompt
                        | self.model
                        | StrOutputParser()
                    )
                )
            )

            conversational_chain = standalone_question_chain | answer_chain

            result = await conversational_chain.ainvoke({
                "question": prompt,
                "chat_history": chat_history,
                "context": context
            })

            response = result['response']
            await self.store_message(sender="bot", text=response)
            return response
        
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            print("Service error")
            raise Exception(f"OpenAI API error: {e}")