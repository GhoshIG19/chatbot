from fastapi import FastAPI
from ai import ai_response


app=FastAPI()

@app.get("/api")
def get_question(query:str):
  answer=ai_response(query)
  
  return answer

