# %%
from openai import OpenAI
import streamlit as st

from dotenv import load_dotenv
import os


# %%
load_dotenv(dotenv_path=".openaidev.env", override=True)  # take environment variables from .env.
# Set the API key and endpoint
api_key = os.getenv('OPENAI_API_KEY')
org = os.getenv('OPENAI_ORG')
project = os.getenv('OPENAI_PROJECT')
model = "gpt-4.1-mini"

# Define the deployment name
deployment_name_embeddings = 'text-embedding-ada-002'

# %%
# OpenAI Client
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


def print_messages(messages=[]):
    for index, message in enumerate(messages):
        print(f"{index}: {message['role']} - {message['content']}")

# %%


def ai_response(messages, model_name='gpt-4o-global'):

    # print(messages)
    """Generator to mimic some LLM response"""
    # response = "This is a long AI generated answer, but I wanted it to stop at the first comma :cry:."
    # for word in response:
    #     yield word
    #     sleep(0.02)

    response = client.responses.create(
        model=model_name,
        input=messages,
        stream=True
    )

    for event in response:
        if event.type == 'response.output_text.delta':
            # print(event.delta)
            yield event.delta


def stream_chat1(messages, model_name='gpt-4o-global'):

    # print("##############################")
    # print_messages(messages)
    # stream = client.chat.completions.create(
    #     model=model_name,
    #     messages=[
    #         {"role": m["role"], "content": m["content"]}
    #         for m in messages
    #     ],
    #     stream=True
    # )

    input = [

        {
            "role": "user",
            "content": [

                    {"type": "input_text", "text": messages},
                    # {
                    #     "type": "input_image",
                    #     "image_url": image_url
                    # }
            ]
        }
    ]
    response_stream = client.responses.create(
        model=model,
        input=input,
        stream=True
    )

    for event in response_stream:
        if event.type == 'response.output_text.delta':
            yield event.delta

    # return response_stream

# def conditional_writer(func: callable)


def user_message(prompt):
    input = {
        "role": "user",
        "content": [

            {"type": "input_text", "text": prompt},
            # {
            #     "type": "input_image",
            #     "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
            # }
        ]
    }

    return input

# %%


st.title("ChatGPT-like clone")

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
    # st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append(user_message(prompt))

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        print(st.session_state.messages)
        stream = ai_response(st.session_state.messages,
                             model_name=st.session_state["openai_model"])
        # # Later update with:
        # message_placeholder.markdown("")

        response = st.write_stream(stream)
        # response = st.markdown('eeee')
        message_placeholder.empty()
    st.session_state.messages.append(
        {"role": "assistant", "content": response})

# %%
