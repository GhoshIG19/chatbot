import json
from pydantic import BaseModel,Field

class Question(BaseModel):
  query: str = Field(examples=["who wins at 2011?"])

def load_db()->list[Question]:
  with open("q.json") as f:
    return [Question.model_validate(obj) for obj in json.load(f)]


def save_db(Questions:list[Question]):
  with open("q.json","w") as f:
    json.dump([Question.model_dump() for Question in Questions],f,indent=4 )

    