from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_database():
   
   try:
     CONNECTION_STRING = os.getenv("CONNECTION_STRING")
     client = MongoClient(CONNECTION_STRING)

     return client['chatbot_db']

   except Exception as e:
      print(f"Cannot connect to MongoDb : {e}")
      raise






  
