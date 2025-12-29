import json
from pydantic import BaseModel,Field

class Question(BaseModel):
  query: str = Field(examples=["who wins at 2011?"])

def load_db()->list[dict]:
  with open("q.json") as f:
    #return [Question.model_validate(obj) for obj in json.load(f)]
    #return [obj for obj in json.load(f)]
    return json.load(f)


def save_db(answers:list[dict]):
  with open("q.json","w") as f:
    #json.dump([Question.model_dump() for Question in Questions],f,indent=4 )
    json.dump(answers,f)
    