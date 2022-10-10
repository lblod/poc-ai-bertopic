from bertopic import BERTopic
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModel

from custom_typing import *

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
    allow_headers=["*"], )

# INIT: loading required models for BERTopic -> these models are loaded from a shared mount.
model = AutoModel.from_pretrained("/models/RobertaModel_PDF_V1")
topic_model = BERTopic.load("/models/topic.model", embedding_model=model)

# Instantiate the topic_info_dataframe, this dataframe contains relevant topic information and is static (precalculated
# During the training of the model)
topic_info_df = topic_model.get_topic_info()


@app.get("/", response_model=health_response, name="Health check route")
async def root():
    """
    This function is a simple health check --> Could be relevant if you are using liveliness/readiness checks.
    """
    return {"status": "healthy"}


@app.get("/get_topic", response_model=get_topics_response, name="This route is made to get the topic for one document")
async def get_topic(input_text: str, ):
    """
    this function calls the get_topics function, the key difference is that in this case we are only sending a request
    containing one input text. For this input text we will get a return that consists out of the predicted model and the
    confidence that it has in this topic beeing a good match.
    """
    return await get_topics([input_text])


@app.get("/get_topics", response_model=get_topics_response,
         name="This route is made to get the topic for multiple documents")
async def get_topics(input_texts: list):
    """
    This function takes a list of input texts, these are processed using the BERTopic framework. After processing we
    receive a topic and a given confidence for this topic for each text.
    """
    topics, probs = topic_model.transform(input_texts)
    return {"result": [{"text": i[0], "topic_id": i[1], "probability": i[2]} for i in zip(input_texts, topics, probs)]}


@app.get("/find_topics", response_model=find_topic_response,
         name="This route will return the most likely topic ids with probability")
async def find_topic(topic_word: str):
    """
    This function returns a list of topics combined with the given confidence score, this confidence score indicates how
    close the match between the search term (user input) and the available topics might be.
    """
    topics, probs = topic_model.find_topics(topic_word)
    return {"result": [{"topic_id": i[0], "probability": i[1]} for i in zip(topics, probs)]}


@app.get("/relevant_docs", response_model=get_relevant_response,
         name="This route will give you the most representative documents for a given topic id")
async def get_docs(topic_id: int):
    """
    This function returns the corpus of a few representative documents, using this function could give a simple
    indication if the found topics are relevant.
    """
    return {"result": topic_model.get_representative_docs(topic_id)}


@app.get("/get_topic_info", response_model=get_topic_info_response,
         name="This route will give you more information for the given topic")
async def get_topic_info(topic_id: int):
    """
    This function will return a few interesting statistics for a given topic. These statistics are the count (Number
    of documents that are within the given topic cluster) and relevant words (these words indicate what the most
    common subject might be within the topic cluster, these are found using tf_idf)
    """
    return {"result": {"topic_id": topic_id, "count": topic_info_df.iloc[topic_id + 1].Count,
        "relevant_words": [{"word": item[0], "score": item[1]} for item in topic_model.get_topics()[topic_id]]}}
