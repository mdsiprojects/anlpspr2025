# %%
from openai import OpenAI
import streamlit as st
from openai import AzureOpenAI

from dotenv import load_dotenv
import os

from helpers.rag import get_system_message, GROUNDED_PROMPT, stream_augmented_generation, user_message


# %%

load_dotenv(override=True)  # take environment variables from .env.
# Set the API key and endpoint
api_key = os.getenv('OPENAI_API_KEY')
org = os.getenv('OPENAI_ORG')
project = os.getenv('OPENAI_PROJECT')
model = "gpt-4o-mini"
deployment_name_embeddings = 'text-embedding-3-small'

# %%
# Azure OpenAI Client
client = OpenAI(
    api_key=api_key,
    organization=org,
    project=project
)

# %%
# initialise session state for the app


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model

if "messages" not in st.session_state:
    st.session_state.messages = []

if 'grounded_prompt' not in st.session_state:
    st.session_state.grounded_prompt = GROUNDED_PROMPT

def print_messages(messages=[]):
    for index, message in enumerate(messages):
        print(f"{index}: {message['role']} - {message['content'][:10]}")


# %%

# Set the page configuration to collapse the sidebar by default
st.set_page_config(
    page_title="RAG Chatbot",
    # layout="wide",
    initial_sidebar_state="collapsed"
)

# Add a sidebar with a text box for the system prompt
system_prompt = st.sidebar.text_area("System Prompt", value=st.session_state.grounded_prompt, height=650)
if system_prompt != st.session_state.grounded_prompt:
    st.session_state.grounded_prompt = system_prompt


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        print("---")
        print(message["role"])
        # print(message["content"])
        print(type(message["content"]))
        # if instance type is list then iterate and print each item
        if isinstance(message["content"], list):
            print("is list")
            print(type(message["content"][0]))
            print(len(message["content"]))
            for i, item in enumerate(message["content"]):
                print(item["text"] if "text" in item else "no text in item")
                print(f"item {i}: {item}")
                st.markdown(item["text"] if "text" in item else "no text in item")
        else:
            print(message["content"])
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append(user_message(prompt))

    with st.chat_message("user"):
        st.markdown(prompt)

    # grounded_input = get_system_message(prompt,metaprompt=system_prompt)
    # st.session_state.messages.append({"role": "system", "content": grounded_input})
    # st.session_state.messages.append({"role": "user", "content": prompt})
    print("############")
    # print(grounded_input)
    print_messages(st.session_state.messages)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        # stream = stream_chat(st.session_state.messages, model_name=st.session_state["openai_model"])
        stream = stream_augmented_generation(
            message_history= st.session_state.messages,
            user_query=prompt,
            model_name=st.session_state["openai_model"]
        )
        response = st.write_stream(stream)
        message_placeholder.empty()
    st.session_state.messages.append({"role": "assistant", "content": response})

# %%






