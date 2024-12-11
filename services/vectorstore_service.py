import asyncio
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import dotenv
from dotenv import load_dotenv
 
load_dotenv()

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
    embeddings_model = OpenAIEmbeddings()
    
    vector_store = InMemoryVectorStore.from_documents(split_texts, embeddings_model)
    
    return vector_store
