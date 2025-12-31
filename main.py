from fastapi import FastAPI,Request,HTTPException
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

@app.get("/api/question/{id}")
def get_quetion_by_id(id:str):
  result=db.get(id)
  if result is not None:
    return result
  else:
    #return {"error":"id is not found"}
    raise HTTPException(status_code=404,detail=f"{id} is not found")

@app.get("/api/questions")
def get_all_quetions():
  l=[]
  for k,v in db.items():
    d={"id":k,"question":v["question"]}
    l.append(d)
  return l

@app.delete("/api/{id}",status_code=204)
def delete_by_id(id:str):
  print("***************",db.keys(),id)
  var=db.pop(id,None)
  if var is not None:
    save_db(db)
    return None
  else:
    raise HTTPException(status_code=404,detail=f"{id} is not found")
  
@app.put("/api/{id}")
def put_by_id(id:str,question:Question):
  print(question)
  if id in db:
    ans=ai_response(question.query)
    db.update({id:{"question":question.query,"result":ans}})
    save_db(db)
    return db[id]
  else:
    raise HTTPException(status_code=404,detail=f"{id} is not found")


# @app.put("api/put/{id}")
# def put_by_id(id:str,question:Question):
#   print(question,"*******************")
#   #if id in db:
#   #  db.update(question)


  
  

      

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

@app.post("/api3",status_code=201)
async def add_question3(question:Question):
  #print(question)
  ans=ai_response(question.query)
  db_len="1"
  if db:
    db_len=str(int(max(db.keys()))+1)
  db.update({db_len:{"result":ans,"question":question.query}})
  save_db(db)
  return ans