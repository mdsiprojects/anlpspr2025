# anlpspr2025
UTS MDSI - ANLP Spring 2025


> It's recommended that you fork this repo to your own GitHub account for your own use, and to get updates from the original repo once posted.

# Monday 29/09/2025

## 📘 Intro

In this code repo and lecture slides we will cover:

- OpenAI API Access
- Azure AI Search
- Anatomy of RAG
- Search data ingestion using a notebook
- Code Samples: responses, chat completion, embeddings and similarity, tools, search methods
- Chat UI with gradio and streamlit
- Putting it all together Chat UI for RAG with streamlit

Lecture material: <img src="https://img.icons8.com/color/48/000000/pdf.png" alt="PDF icon" width="24" height="24"/> [coming soon!](<comingsoon.pdf>)

## 🐍 Installing openao python SDK

You can use the `venv` module (or conda) to create a python env

Create a Virtual Environment with venv:  `python -m venv .venv`

Activate the Environment:

- On Windows: `.venv\Scripts\activate`
- On macOS/Linux: `source .venv/bin/activate`

install openai using pip: `pip install openai`

Alternatively, create a requirements.txt file with all dependencies: `pip install –r requirements.txt`

Sample [requirements.txt](<requirements.txt>) file is provided in the repo.


## 🤖 How to use OpenAI SDK

Import Azure OpenAI from the openai library:
```python
from openai import OpenAI
```

To create vector embeddings import the embeddings module:

```python
from openai import embeddings
```

Create and Azure OpenAI client:

```python
client = OpenAI(
    api_key=api_key,
    organization=org,
    project=project
)
```

Get your api_key, org and project from the OpenAI platform dashboard portal (https://platform.openai.com/account/api-keys).

### 💬 Responses API
You will use the Responses API to interact with the openai models:
https://platform.openai.com/docs/api-reference/responses/create?lang=python


```python
response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {"role": "assistant", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"}
    ]
)

print(response.output_text)
```

### 📊 Vector Embeddings
Using the client embeddings function to create vector embeddings:

```python
embedding = client.embeddings.create(
    model=embedding_model,
    input=["Hello, world!", "Hola!"]
)

for e in embedding.data:
    print(e.embedding)
```

## 🖥️ Using Streamlit with VS Code

Install streamlit and demo app: https://docs.streamlit.io/get-started/installation/command-line
Streamlit chat app tutorial: https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps

Test the installation of `streamlit` by running the following command in your terminal:

```bash
python -m streamlit hello
```

To debug `streamlit` apps, add the follow to your `launch.json` file:

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: streamlit Module",
            "type": "debugpy",
            "request": "launch",
            "module": "streamlit",
            "args": ["run", "${file}"],
        }
    ]
}
```




