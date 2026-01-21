from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from scrapping import response_get_markdown
from ai_embedding import get_embeddings,cosine_similarity,get_embeddings_local




# Step 1: Split by Headers
# This keeps text under the same header together and adds headers to metadata
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3")
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on,strip_headers=False)


# # 2. Initialize the splitter
# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=200,       # The target size of each chunk
#     chunk_overlap=0,     # The amount of shared text between adjacent chunks
#     length_function=len,   # How to measure length (usually characters)
#     is_separator_regex=False,
# )

# 3. Create the chunks
def get_top_similar_chunks(text:str, query:str, top_n:int=3)->list[str]:
    
    chunks = splitter.split_text(text)
    chunks_page_content=[]
    # Check the results
    for chunk in chunks:
      chunks_page_content.append(chunk.page_content)
    #print(chunks_page_content)
    response_query=get_embeddings(query)
    #print(response_query.data[0].embedding[:5])
    scores=[]
    top_chunks=[]
    response=get_embeddings(chunks_page_content)
    for i,data in enumerate(response.data):
        #print(data.embedding[:5])
        score = cosine_similarity(data.embedding,response_query.data[0].embedding)
        #print(score)
        #   if score>0.35:
        #     print(i,score)
        #     print(chunks_page_content[i])
        scores.append((score,chunks_page_content[i]))
    
    scores.sort(reverse=True)
    #scores2=sorted(scores,reverse=True)
    #print(scores[0:top_n])
    for t in scores[0:top_n]:
      top_chunks.append(t[1])
      
    return top_chunks

    
    # print(f"Created {len(chunks)} chunks.")
    # print(f"First chunk sample: {chunks[0]}")
    # print(f"Second chunk sample: {chunks[1]}")
    # print(f"Third chunk sample: {chunks[2]}")
    # print(f"Fourth chunk sample: {chunks[3]}")
    # print(f"Fifth chunk sample: {chunks[4]}")
    # print(f"Sixth chunk sample: {chunks[5]}")

def get_top_similar_chunks_local(text:str, query:str, top_n:int=3)->list[str]:
    
    chunks = splitter.split_text(text)
    chunks_page_content=[]
    # Check the results
    for chunk in chunks:
      chunks_page_content.append(chunk.page_content)
    #print(chunks_page_content)
    response_query=get_embeddings_local(query)
    #print(response_query.data[0].embedding[:5])
    scores=[]
    top_chunks=[]
    response=get_embeddings_local(chunks_page_content)
    for i,embedding in enumerate(response):
        #print(data.embedding[:5])
        score = cosine_similarity(embedding,response_query)
        #print(score)
        #   if score>0.35:
        #     print(i,score)
        #     print(chunks_page_content[i])
        scores.append((score,chunks_page_content[i]))
    
    scores.sort(reverse=True)
    #scores2=sorted(scores,reverse=True)
    #print(scores[0:top_n])
    for t in scores[0:top_n]:
      top_chunks.append(t[1])
      
    return top_chunks
if __name__=="__main__":
  # 1. Load your document text
  text=response_get_markdown(url = 'https://lnkk.in/icc-mens-cricket-world-cup-odi/')
  #print(text)
  query="who wins world cup at 2011?"
  #query="who wins at 2011?"
  print(get_top_similar_chunks(text,query,5))