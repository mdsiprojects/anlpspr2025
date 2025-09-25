# %%
from openai import OpenAI
from openai import embeddings
from dotenv import load_dotenv

from IPython.display import Markdown, display


from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
import os

from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery, VectorQuery, VectorizedQuery, QueryType

load_dotenv(dotenv_path=".openaidev.env")
# %%

endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
credential = AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"]) if len(os.environ["AZURE_SEARCH_ADMIN_KEY"]) > 0 else DefaultAzureCredential()
index_name = os.environ["AZURE_SEARCH_INDEX"]

# Set the API key and endpoint
api_key = os.getenv('OPENAI_API_KEY')
org = os.getenv('OPENAI_ORG')
project = os.getenv('OPENAI_PROJECT')
# model = "gpt-5-mini-2025-08-07"
embedding_model = "text-embedding-3-small"
model = "gpt-5-mini"

# Set query parameters for grounding the conversation on your search index
search_type="text"
use_semantic_reranker=True
sources_to_include=5


# %%
client = OpenAI(
    api_key=api_key,
    organization=org,
    project=project
)

# %%
search_client = SearchClient(
    endpoint,
    index_name,
    credential=credential)

# %%

def generate_embeddings(text):
    client = OpenAI(
        api_key=api_key,
        organization=org,
        project=project
    )

    embedding = client.embeddings.create(
        model=embedding_model,
        input=text
    )
    embedding = embedding.data[0].embedding
    return embedding

# %%
# define a search function

def search_function(query_text, top_k=5, vector_only=False):
    vector = generate_embeddings(query_text)
    vector_query = VectorizedQuery(
        vector=vector,
        k_nearest_neighbors=top_k,
        fields="content_vector",
        exhaustive=True,
    )

    search_client = SearchClient(
        endpoint,
        index_name,
        credential=credential)

    search_text = None if vector_only else query_text
    results = search_client.search(
        search_text=search_text,
        vector_queries=[vector_query],
        select=["chunk_id", "file_name", "base_name", "content", "content_vector"],
        top=top_k,
        include_total_count=True,
        # query_type=QueryType.FULL,
        semantic_configuration_name="my-semantic-config",
    )
    return results

# %%
# This prompt provides instructions to the model
GROUNDED_PROMPT="""
 # PURPOSE:
 You are a friendly assistant that answer questions from company's HR policy and information documents.
 Answer the query using only the sources provided below in a friendly and concise bulleted manner.
 Answer ONLY with the facts listed in the list of sources below.
 If there isn't enough information below, say you don't know.
 Do not generate answers that don't use the sources below.

 # CITATION:
 - Always include source in brackets in the response from list of sources below.
 - If you use multiple sources, cite them all in brackets in the response.
 - include a list of sources as a foot note in bullet points format.
 - Only include sources that were used to generate the answer.
 - dont display any sources or sources section if it was not cited in response

 example list of sources:
 ### Sources:
 - SOURCE NO 1. filename1.pdf(chunk id number))
 - SOURCE NO 2. filename2.pdf(3)
 - SOURCE NO 3. filename3.pdf(5)

 # Sources:
 \n{sources}

"""
# %%
#extract user search intent
SEARCH_INTENT_PROMPT = """
You are asked to read the user query, understand it, and then turn it into a search query.
The search query should be sent to the search engine to find the relevant information.
the search query should be similar to what a user would type into a search engine, and similar in meaning to the provided user query.
the user query is: '{user_query}'
return only the search query text. """


# %%
#extract user search intent


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

def extract_search_intent(user_query="Is pregnancy going to be covered by my health plan?"):
    # print(SEARCH_INTENT_PROMPT.format(user_query=user_query))

    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SEARCH_INTENT_PROMPT.format(user_query=user_query)},
        ]
    )

    search_query = response.output_text

    return search_query

# %%
 # Retrieve the selected fields from the search index related to the question.

def get_search_results(
        text_query="Is pregnancy going to be covered by my health plan?",
        search_type="text",
        use_semantic_reranker=True,
        sources_to_include=5):



    results = search_function(
        query_text=text_query,
        top_k=sources_to_include
    )


    list_of_sources = [
        f'\nSOURCE NO {index + 1}. {result["base_name"]}({result["chunk_id"]}): {result["content"]} )'
        for index, result in enumerate(results)
        ]

    print("##### SOURCES ######")
    print(len(list_of_sources))
    joined_sources = "\n".join(list_of_sources)
    # print(joined_sources)

    return joined_sources



def get_system_message(user_query, metaprompt=GROUNDED_PROMPT):
    print(f"##### get system message, User Query: {user_query}")
    # search_query = extract_search_intent(user_query)
    search_query = user_query
    sources = get_search_results(search_query)


    grounded_input = metaprompt.format(sources=sources)
    return grounded_input


def get_augmented_generation(user_query, metaprompt):

    grounded_input = get_system_message(user_query, metaprompt)

    response = client.responses.create(
        model=model,
        intput=[
            {"role": "system", "content": grounded_input},
            {"role": "user", "content": user_query}
        ]
    )


    final_response = response.output_text

    return final_response


def stream_augmented_generation(message_history, user_query, metaprompt=GROUNDED_PROMPT, model_name=model):
    print("########### STREAM AUGMENTED GENERATION ############")
    grounded_input = get_system_message(user_query, metaprompt)
    # print(grounded_input)
    # print(user_query)
    input = []
    input.extend(message_history)
    input.append({"role": "system", "content": grounded_input})
    input.append({"role": "user", "content": user_query})


    for i in input:
        print(i["role"], " - ", i["content"][:50] if isinstance(i["content"], str) else "list content")
    print("##### FINAL INPUT TO RAG MODEL #####")
    print(model_name)
    response = client.responses.create(
        model=model_name,
        input=input,
        stream=True
    )

    for event in response:
        if event.type == 'response.output_text.delta':
            # print(event.delta)
            yield event.delta




