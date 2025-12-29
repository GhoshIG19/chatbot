from fastapi import FastAPI,Request
from ai import ai_response
import json
from schemas import load_db,save_db,Question

app=FastAPI()
db=load_db()
print("db",db)

@app.get("/api")
def get_question(query:str):
  ans=ai_response(query)
  
  return ans

@app.post("/api")
async def add_question(request:Request):
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

@app.post("/api3")
async def add_question3(question:Question):
  #print(question)
  ans=ai_response(question.query)
  db.append({"result":ans})
  save_db(db)
  return ans