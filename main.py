import uuid
import json
from fastapi import FastAPI,Request,HTTPException
from ai import ai_response
from schemas import load_db,save_db,Question
from data.nosql.mongodb_connection import get_mongodb_connection
from bson.objectid import ObjectId

app=FastAPI()
db=load_db()
print("db",db)

@app.get("/api")
def get_question(query:str):
  ans=ai_response(query)
  
  return ans

@app.get("/api/questions")
def get_all_quetions():
  l=[]
  for k,v in db.items():
    d={"id":v["_id"],"question":v["question"]}
    l.append(d)
  return l

@app.get("/api/question/{id}")
def get_quetion_by_id(id:str):
  #result=db.get(id)
  with get_mongodb_connection() as client:
      db=client.chatbot
      result=db.chat_conversations.find_one({"_id":ObjectId(id)})
 
  if result is not None:
    result.update({"_id":str(result["_id"])})
    return result
  else:
    #return {"error":"id is not found"}
    raise HTTPException(status_code=404,detail=f"{id} is not found")



@app.delete("/api/{id}",status_code=204)
def delete_by_id(id:str):
   with get_mongodb_connection() as client:
      db=client.chatbot
      result=db.chat_conversations.delete_one({"_id":ObjectId(id)})
   #print(result.deleted_count,dir(result))   
   if result.deleted_count !=0:
    return None
   else:
    raise HTTPException(status_code=404,detail=f"{id} is not found")
  # print("***************",db.keys(),id)
  # var=db.pop(id,None)
  # if var is not None:
  #   save_db(db)
  #   return None
  # else:
  #   raise HTTPException(status_code=404,detail=f"{id} is not found")
  
@app.put("/api/{id}")
def put_by_id(id:str,question:Question):
  # print(question)
  # if id in db:
  #   ans=ai_response(question.query)
  #   db.update({id:{"question":question.query,"result":ans}})
  #   save_db(db)
  #   return db[id]
  # else:
  #   raise HTTPException(status_code=404,detail=f"{id} is not found")
   ans=ai_response(question.query)
   with get_mongodb_connection() as client:
      db=client.chatbot
      result=db.chat_conversations.update_one({"_id":ObjectId(id)},{"$set":{"question":question.query,"result":ans}})
   #print("***********",result,dir(result))
   if result.matched_count != 0 and result.modified_count != 0:
      with get_mongodb_connection() as client:
        db=client.chatbot
        result2=db.chat_conversations.find_one({"_id":ObjectId(id)})
      if result2 is not None:
        result2.update({"_id":str(result2["_id"])})
        return result2
      else:
        raise HTTPException(status_code=404,detail=f"{id} is not found")
   elif(result.matched_count != 0):
     raise HTTPException(status_code=404,detail=f"{id} is not modified")
   else:
     raise HTTPException(status_code=404,detail=f"{id} is not found")
     
@app.post("/api3")
async def add_question3(request:Request):
  request_body=await request.body()

  question=json.loads(request_body.decode()).get("query")
  
  if question is not None:
    if type(question) is str:
      ans=ai_response(question)
      return ans
    else:
      return {"error":"query is not string"}
  else:
    return {"error":"query is not provided"}

@app.post("/api2")
async def add_question2(request:Request):
  request_body=await request.body()
  request_dict=json.loads(request_body.decode())
  #print(request_dict)
  q=Question(**request_dict)
  #print(q)
  ans=ai_response(q.query)
  return ans

@app.post("/api",status_code=201)
async def add_question(question:Question):
  #print(question)
  ans=ai_response(question.query)
  # db_len="1"
  # if db:
  #   db_len=str(int(max(db.keys()))+1)
  # _id=uuid.uuid4().hex
  # db.update({_id:{"_id":_id,"result":ans,"question":question.query}})
  # save_db(db)
  question_answer={"question":question.query,"result":ans}
  with get_mongodb_connection() as client:
      db=client.chatbot
      collection=db.chat_conversations
      collection.insert_one(question_answer)
  question_answer.update({"_id":str(question_answer["_id"])})    
  return question_answer