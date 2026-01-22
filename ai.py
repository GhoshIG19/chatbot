import os
import ollama
from openai import OpenAI
from dotenv import load_dotenv
from scrapping import response_get_markdown
from create_chunks import get_top_similar_chunks,get_top_similar_chunks_local

# 1. Load the token from the .env file


load_dotenv()
token = os.environ.get("GITHUB_TOKEN")
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY")

if not OLLAMA_API_KEY:
    raise ValueError("token not found. Please set OLLAMA_API_KEY in your .env file.")

if not token:
    raise ValueError("Token not found. Please set GITHUB_TOKEN in your .env file.")


endpoint = "https://models.github.ai/inference"
endpoint_ollama="https://ollama.com"
#model_name = "gpt-4o" 
model_name = "openai/gpt-4.1"
model_name_local_ollama="gemma3:4b"
model_name_cloud_ollama="gemma3:27b-cloud"

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

#client_ollama=ollama.Client(host=endpoint_ollama, headers={'Authorization': f'Bearer {OLLAMA_API_KEY}'})
# <OR>
client_ollama=ollama.Client(host=endpoint_ollama)
# 3. Define the model you want to use
# Check https://github.com/marketplace/models for exact model names

def ai_response(user_query:str)->str:
    url = 'https://lnkk.in/icc-mens-cricket-world-cup-odi/'
    response_markdown2=response_get_markdown(url)
    #print(response_markdown2)
    top_chunk_text="\n\n".join(get_top_similar_chunks_local(response_markdown2,user_query))
    # prompt={
    #     "role": "user",
    #     "content": f"context: {response_markdown2} \nquestion: {user_query}",
    #     }
    prompt={
        "role": "user",
        "content": f"context: {top_chunk_text} \nquestion: {user_query}",
        }
    print(prompt)
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
    
def ai_response_local_ollama(user_query:str)->str:
    url = 'https://lnkk.in/icc-mens-cricket-world-cup-odi/'
    response_markdown2=response_get_markdown(url)
    #print(response_markdown2)
    top_chunk_text="\n\n".join(get_top_similar_chunks_local(response_markdown2,user_query))
    # prompt={
    #     "role": "user",
    #     "content": f"context: {response_markdown2} \nquestion: {user_query}",
    #     }
    prompt={
        "role": "user",
        "content": f"context: {top_chunk_text} \nquestion: {user_query}",
        }
    print(prompt)
    try:
        result=""
        #print(f"Talking to {model_name} via GitHub Models...\n")
        
        response = ollama.chat(
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
            model=model_name_local_ollama,
            #temperature=0.0,
            #max_tokens=1000,
        )
        result=response["message"]["content"]

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
      return  result

   
def ai_response_cloud_ollama(user_query:str)->str:
    url = 'https://lnkk.in/icc-mens-cricket-world-cup-odi/'
    response_markdown2=response_get_markdown(url)
    #print(response_markdown2)
    top_chunk_text="\n\n".join(get_top_similar_chunks_local(response_markdown2,user_query))
    # prompt={
    #     "role": "user",
    #     "content": f"context: {response_markdown2} \nquestion: {user_query}",
    #     }
    prompt={
        "role": "user",
        "content": f"context: {top_chunk_text} \nquestion: {user_query}",
        }
    print(prompt)
    try:
        result=""
        #print(f"Talking to {model_name} via GitHub Models...\n")
        
        response = client_ollama.chat(
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
            model=model_name_cloud_ollama,
            #temperature=0.0,
            #max_tokens=1000,
        )
        result=response["message"]["content"]

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
      return  result

if __name__=="__main__":
  #print(ai_response(user_query= "who wins world cup in 2011"))
  #response = ollama.generate(model=model_name_local_ollama, prompt='What is the capital of West Bengal?')
  #print(response['response'])
  #print(ai_response_local_ollama(user_query= "who wins world cup in 2011?"))
  print(ai_response_cloud_ollama(user_query= "who wins world cup in 2011?"))
  