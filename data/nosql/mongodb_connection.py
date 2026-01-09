import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from contextlib import contextmanager
 

load_dotenv()

conection_string_url = os.environ.get("MONGODB_DOCKER_URL")
if not conection_string_url:
    raise ValueError("Token not found. Please set MONGODB_DOCKER_URL in your .env file.")

database_name=conection_string_url.split("/")[-1]
@contextmanager
def get_mongodb_connection(url:str=conection_string_url):
    try:
      client=MongoClient(url)
      print("--- Connection Opened ---")
      yield client
    except ConnectionFailure as cf:
      print(cf,"exiting")
      exit()
    finally:
       client.close()
       print("--- Connection Terminated Safely ---")

if __name__=="__main__":
    # client=MongoClient(conection_string_url)
    # for db_name in client.list_database_names():
    #     print(db_name)
    # db=client.chatbot
    # collection=db.chat_conversations
    # result=collection.insert_one({"question":"test","result":"test"})
    # print(result)
    # client.close()

    with get_mongodb_connection(conection_string_url) as client:
      db=client.chatbot
      collection=db.chat_conversations
      result=collection.insert_one({"question":"test2","result":"test2"})
      print(result)

