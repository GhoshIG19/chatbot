import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv


#print(os.environ.get("GITHUB_TOKEN"),"before")
load_dotenv()
#print(os.environ.get("GITHUB_TOKEN"),"after")
endpoint = "https://models.github.ai/inference"
#endpoint="https://models.inference.ai.azure.com"


def cosine_similarity(vec1, vec2):
    # Convert lists to numpy arrays
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    
    # Formula: dot(v1, v2) / (norm(v1) * norm(v2))
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    return dot_product / (norm_v1 * norm_v2)

#input=["Hello, how do I use GitHub models?", "Hello, how do I use GitHub models?"]

#input=["Berlin is the capital of Germany. It has a population of 3.6 million.", "What is the capital of Germany?"]

#input=["Berlin is the capital of Germany. It has a population of 3.6 million.", "What is the population of capital of Germany?"]

input=["Berlin is the capital of Germany. It has a population of 3.6 million.", "What is the capital of France?"]

# input=["cat", "dog"]
#input=["puppy","dog"]
#input=["fish","dog"]
#input=["lion","dog"]
#input=["ocean","dog"]
#input=["paris","capital of france"]
#input=["kolkata","capital of france"]
#input=["paris","dog"]
def get_embeddings(input:list[str] | str):
    client = OpenAI(
        base_url=endpoint,
        api_key=os.environ.get("GITHUB_TOKEN")
    )
    # 2. Call the embeddings API
    response = client.embeddings.create(
        input=input,
        model="text-embedding-3-small"
    )
    return response

if __name__=="__main__":
    response=get_embeddings(input)

    # 3. Access the embedding vectors
    for i, data in enumerate(response.data):
        print(f"Embedding for string {i}: {data.embedding[:5]}... (length: {len(data.embedding)})")
    print(response.data[0].embedding==response.data[1].embedding)
    emb1=response.data[0].embedding
    emb2=response.data[1].embedding
    score = cosine_similarity(emb1, emb2)
    print(f"Similarity Score: {score:.4f}")
    