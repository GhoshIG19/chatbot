import os
from openai import OpenAI
from dotenv import load_dotenv
from scrapping import response_get_markdown
# 1. Load the token from the .env file

load_dotenv()
token = os.environ.get("GITHUB_TOKEN")

if not token:
    raise ValueError("Token not found. Please set GITHUB_TOKEN in your .env file.")


endpoint = "https://models.github.ai/inference"
#model_name = "gpt-4o" 
model_name = "openai/gpt-4.1"
#
# 2. Initialize the client pointing to GitHub's endpoint
#client = OpenAI(
#    base_url="https://models.inference.ai.azure.com",
#    api_key=token,
#)
## OR
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# 3. Define the model you want to use
# Check https://github.com/marketplace/models for exact model names

def ai_response(user_query:str)->str:
    url = 'https://lnkk.in/icc-mens-cricket-world-cup-odi/'
    response_markdown2=response_get_markdown(url)
    #print(response_markdown2)
    
    prompt={
        "role": "user",
        "content": f"context: {response_markdown2} \nquestion: {user_query}",
        }
    try:
        result=""
        #print(f"Talking to {model_name} via GitHub Models...\n")
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful assistant.
                                Rules:
                                1. You must answer the user's question using ONLY the context provided. 
                                2. Do NOT use your internal traing data, common sense, or prior knowledge.
                                3. If the answer is not present in the context, strictly output: "I can not answer this based on the provided context."
                                """,
                },
                # {
                #     "role": "user",
                #     "content": "what is the capital of west bengal?",
                # },
                prompt
            ],
            model=model_name,
            temperature=1.0,
            max_tokens=1000,
        )

        #print("Response:")
        #print(response.choices[0].message.content)
        result=response.choices[0].message.content

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
      return  result


if __name__=="__main__":
  print(ai_response(user_query= "who wins world cup in 2011"))