UTS MDSI - ANLP Spring 2025
Monday 29/09/2025

- [📘 Intro](#-intro)
- [🐍 Installing OpenAI python SDK](#-installing-openai-python-sdk)
- [🤖 How to use OpenAI SDK](#-how-to-use-openai-sdk)
  - [💬 Responses API](#-responses-api)
  - [📊 Vector Embeddings](#-vector-embeddings)
- [🖥️ Using Streamlit with VS Code](#️-using-streamlit-with-vs-code)
- [🦙 Using Ollama and Offline Models](#-using-ollama-and-offline-models)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
- [☁️ Getting Azure AI Student Subscription \& Provisioning Services](#️-getting-azure-ai-student-subscription--provisioning-services)
  - [1. Get an Azure for Students Subscription](#1-get-an-azure-for-students-subscription)
  - [2. Provision Azure AI Search (Free Tier)](#2-provision-azure-ai-search-free-tier)
  - [3. Provision Azure AI Document Intelligence (Form Recognizer)](#3-provision-azure-ai-document-intelligence-form-recognizer)
  - [4. Get Your Keys and Endpoints](#4-get-your-keys-and-endpoints)


> It's recommended that you fork this repo to your own GitHub account for your own use, and to get updates from the original repo once posted.



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

## 🐍 Installing OpenAI python SDK

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


## 🦙 Using Ollama and Offline Models

Ollama lets you run large language models locally on your machine, enabling offline inference and experimentation with open-source models.

### Installation

- **Windows/macOS/Linux:**
    - Visit the [Ollama download page](https://ollama.com/download) and follow the instructions for your operating system.
    - Alternatively, on macOS you can use Homebrew: `brew install ollama`

### Basic Usage

After installing, you can pull and run a model (e.g., llama3) with:

```sh
ollama pull llama3
ollama run llama3
```

You can interact with the model in your terminal, or use the Ollama API to connect from Python or other tools.



## ☁️ Getting Azure AI Student Subscription & Provisioning Services

To use Azure AI Search and Azure AI Document Intelligence, you need an Azure subscription. Students can get free Azure credits and services:

### 1. Get an Azure for Students Subscription

- Visit the [Azure for Students page](https://azure.microsoft.com/free/students/) and sign up with your university email.
- You’ll receive free credits and access to popular services, no credit card required.

### 2. Provision Azure AI Search (Free Tier)

1. Go to the [Azure Portal](https://portal.azure.com/).
2. Click **Create a resource** > search for **Azure AI Search**.
3. Click **Create** and fill in the required details:
    - **Resource group**: Create new or use existing
    - **Service name**: Choose a unique name
    - **Region**: Select a region
    - **Pricing tier**: Select **Free** (limits apply)
4. Click **Review + create** and then **Create**.

### 3. Provision Azure AI Document Intelligence (Form Recognizer)

1. In the Azure Portal, click **Create a resource** > search for **Azure AI Document Intelligence** (or **Form Recognizer**).
2. Click **Create** and fill in the required details:
    - **Resource group**: Use the same or new
    - **Region**: Select a region
    - **Pricing tier**: Free F0 (limited pages per request)
    - **Resource name**: Choose a unique name
3. Click **Review + create** and then **Create**.

### 4. Get Your Keys and Endpoints

After deployment, go to each resource and find the **Keys and Endpoint** section. You’ll need these values to connect your code to Azure services.

**Tip:** Store your keys in a `.env` file and never share them publicly.




