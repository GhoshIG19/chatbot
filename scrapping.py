from bs4 import BeautifulSoup
from markdownify import markdownify as md
import requests
import re
import sys
def response_get_markdown(url:str)-> str:
    try:
        markdown_text=""
        # Attempt to connect to the website
        response = requests.get(url, timeout=10) # Good practice to add a timeout
        response.raise_for_status() # Raises an error if the status is 404 or 500

        print(f"Status Code: {response.status_code} #####################")

        soup = BeautifulSoup(response.text, features="html.parser")
        
        # Define regex for ID
        id_pattern = re.compile(r'^post')

        # Find the article
        article = soup.find("article", id=id_pattern)

        if article:
            # Convert ONLY the article to markdown
            markdown_text = md(str(article), heading_style="ATX")
            #print("\n--- MARKDOWN OUTPUT ---\n")
            #print(markdown_text)
        else:
            print("Could not find the article with that ID.")

    except requests.exceptions.ConnectionError:
        print("\n[!] CRITICAL ERROR: Could not connect to the internet or the website.")
        print("    Please check your Wifi/Ethernet connection.")
    except requests.exceptions.Timeout:
        print("\n[!] ERROR: The request timed out. The server might be slow.")
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
    finally:
        return markdown_text

#print(__name__)
if __name__=="__main__":
  print(response_get_markdown(url = 'https://lnkk.in/icc-mens-cricket-world-cup-odi/'))