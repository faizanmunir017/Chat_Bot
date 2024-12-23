
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from pinecone import Pinecone, ServerlessSpec
import time
import os
 
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
cloud ='aws'
region ='us-east-1'
spec = ServerlessSpec(cloud=cloud, region=region)

INDEX_NAME = "chatbot-index"
NAMESPACE = "chatbot-namespace"

pinecone = Pinecone(api_key=PINECONE_API_KEY)

if INDEX_NAME not in pinecone.list_indexes().names():
    pinecone.create_index(
        name=INDEX_NAME,
        dimension=1024, 
        metric="cosine",
        spec=spec,
    )
    while not pinecone.describe_index(INDEX_NAME).status["ready"]:
        time.sleep(1)

index = pinecone.Index(INDEX_NAME)

def load_pages(file_path):
    loader = PyPDFLoader(file_path)
    pages=loader.load()
    return pages

def create_vector_store(file_path):
    pages = load_pages(file_path)  
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len
    )

    split_texts = text_splitter.split_documents(pages) 
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=os.getenv("OPENAI_API_KEY"))
    vector_store = PineconeVectorStore.from_documents(
        documents=split_texts,
        index_name=INDEX_NAME,
        embedding=embeddings,
        namespace=NAMESPACE,
    )
    
    retriever = vector_store.as_retriever()
    return vector_store, retriever
    

