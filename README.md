Using GitHub Models (which allows you to access models like GPT-4o, Llama 3, and Mistral via a free API) with `uv` (a fast Python project manager) is a modern and efficient workflow.

Here is the step-by-step procedure to set this up.

### Prerequisites

* **GitHub Account:** You need an active GitHub account.
* **uv Installed:** If you haven't installed `uv` yet, run this in your terminal:
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

```



---

### Step 1: Get Your GitHub Personal Access Token

You need a token to authenticate with the GitHub Models API.

1. Go to the [GitHub Marketplace Models page](https://github.com/marketplace/models).
2. Click on any model (e.g., **GPT-4o** or **Llama-3**).
3. Click the green **"Playground"** button.
4. In the playground, look for a **"Get started"** or **"Get token"** link (usually near the code snippets).
* *Alternatively:* Go to your GitHub Settings > **Developer settings** > **Personal access tokens** > **Tokens (classic)**.
* Generate a new token with the **`read:user`** scope (some models might require no specific scope, but `read:user` is standard for authentication).


5. **Copy the token** and save it safely. You will need it in Step 5.

### Step 2: Initialize a New Python Project with `uv`

Open your terminal and create a fresh, isolated project.

1. Create and initialize the project directory:
```bash
uv python install 3.12
uv python pin 3.12
uv run python --version
uv init github-models-demo
cd github-models-demo

```


*This creates a `pyproject.toml` file and a default `hello.py` script.*

### Step 3: Add Dependencies

GitHub Models uses the standard OpenAI SDK for Python (it is API-compatible). You will also likely want `python-dotenv` to manage your secrets securely.

1. Run the following command:
```bash
uv add openai python-dotenv

```


*`uv` will automatically create a virtual environment (`.venv`), resolve versions, and install these libraries.*

### Step 4: Configure Your Environment Variables

**Never hardcode your token in your script.** Instead, use a `.env` file.

1. Create a file named `.env` in your project folder.
2. Add your token to it:
```env
GITHUB_TOKEN=ghp_your_token_here_...

```



### Step 5: Write the Code

Create a new file named `main.py` (or edit the existing `hello.py`) and paste the following code.

**Note:** The endpoint `https://models.inference.ai.azure.com` is the standard gateway for GitHub Models.

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load the token from the .env file
load_dotenv()
token = os.environ.get("GITHUB_TOKEN")

if not token:
    raise ValueError("Token not found. Please set GITHUB_TOKEN in your .env file.")

# 2. Initialize the client pointing to GitHub's endpoint
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=token,
)

# 3. Define the model you want to use
# Check https://github.com/marketplace/models for exact model names
model_name = "gpt-4o" 

try:
    print(f"Talking to {model_name} via GitHub Models...\n")
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful Python expert.",
            },
            {
                "role": "user",
                "content": "Explain briefly why 'uv' is faster than pip.",
            },
        ],
        model=model_name,
        temperature=1.0,
        max_tokens=1000,
    )

    print("Response:")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"An error occurred: {e}")

```

### Step 6: Run the Project

Use `uv run` to execute your script within the isolated environment it created.

```bash
uv run main.py

```

### Summary of Commands

Here is the cheat sheet for the entire process:

```bash
# 1. Setup
uv init my-ai-app
cd my-ai-app
uv add openai python-dotenv
uv add fastapi[all]
uv add requests httpx beautifulsoup4
uv add markdownify 

# 2. Setup Env
# (Create .env file manually and paste GITHUB_TOKEN=...)

# 3. Run
uv run main.py
uv run fastapi dev main.py
```

### Troubleshooting

* **Model not found?** Ensure the `model_name` in your Python script matches exactly what is listed in the GitHub Marketplace (e.g., `Meta-Llama-3.1-8B-Instruct`).
* **Rate Limits:** The free tier of GitHub Models has strict rate limits (requests per minute). If you see a 429 error, wait a minute and try again.

... [How to use Python UV: The New BLAZINGLY FAST Package Manager (Quickstart Guide)](https://www.youtube.com/watch?v=QKVQQCx-gi4)

This video is relevant because it provides a visual walkthrough of the `uv` commands used in this guide, helping you understand how `uv init`, `uv add`, and `uv run` work in practice.