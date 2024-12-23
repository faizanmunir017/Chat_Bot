
from openai import OpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langsmith import traceable
from langchain.schema.retriever import BaseRetriever
from pymongo.collection import Collection
from utils.constant import chat_instructions
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from utils.chat_helper import store_message, get_last_messages, summarize_context
from typing import List
from langchain_pinecone import PineconeVectorStore

class ChatService:   
    def __init__(self, api_key: str, vector_store: PineconeVectorStore, retriever: BaseRetriever, db_collection: Collection):
        self.model = ChatOpenAI(api_key=api_key, model="gpt-4o-mini", temperature=0.7)
        self.vector_store = vector_store 
        self.retriever = retriever
        self.collection = db_collection
        self.condense_question_prompt = PromptTemplate.from_template(chat_instructions["condense_question_prompt"])
        self.answer_prompt = PromptTemplate.from_template(chat_instructions["answer_prompt"])

    @traceable(project_name="ChatBot_Interactions")
    async def chat_with_gpt(self, prompt: str) -> str:
        try:
            print("In chat with gpt")
            await store_message(sender="user", text=prompt, collection=self.collection)
            
            docs = await self.retriever.aget_relevant_documents(prompt)
            full_context = "\n".join([doc.page_content for doc in docs])
            context = await summarize_context(full_context, self.model)

            chat_history = await get_last_messages(self.collection)

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
            await store_message(sender="bot", text=response, collection=self.collection)
            return response

        except Exception as e:
            print(f"OpenAI API Error: {e}")
            print("Service error")
            raise Exception(f"OpenAI API error: {e}")
