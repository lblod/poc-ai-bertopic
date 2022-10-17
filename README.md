# poc-ai-bertopic-api
This repository contains the fast-api code for the bertopic API,

## Getting started
In order to run this code, you will either have to build it localy or use our build container. Keep in mind you will have to supply the container with our model (you can copy it from a google storage bucket).

### COPY model from GCP bucket
An easy way to download files from a google cloud bucket, is by installing the gsultil client, You can find more information on how to install this client [here](https://cloud.google.com/storage/docs/gsutil_install).

Gsutil command(s):
```
gsutil -m cp -r gs://abb-textgen-models/topioc.model .
gsutil -m cp -r gs://abb-textgen-models/RobertaModel_PDF_V1 .
```

### Starting the docker container
First you pull the container (can be skipped --> will be pulled either if not present when executing the run command)
```
docker pull lblod/poc-ai-embed
```

Once the container is pulled, you can start it using the following command
```
docker run -it --rm  -v <folder_container_model>:/models/ -p 8080:8080 lblod/poc-ai-bertopic
```

## API routes

### /get_topic
This function is used to get a prediction on what topic the given text is linked to. Underling this code passes the input text
through to the /get_topics function as a list.

Example return schema:
```
{
  "result": [
    {
      "text": "string",
      "topic_id": 0,
      "probability": 0
    }
  ]
}
```

### /get_topics
This function takes a list of input texts, these will be processed using the BERTopic framework. This processing will return a topic per text
in the collection of texts that were provided.

Example return schema:
```
{
  "result": [
    {
      "text": "string",
      "topic_id": 0,
      "probability": 0
    }
  ]
}
```
### /find_topics
This function returns a list of topics combined with the given confidence score, this confidence score indicates how close the match between the search term (user input) and the found topics is.

Example return schema:
```
{
  "result": [
    {
      "topic_id": 0,
      "probability": 0
    }
  ]
}
```

### /relevant_docs
This function returns the corpus of a 3 representative documents, using this function could give a simple indication if the found topics are relevant.

Example return schema:
```
{
  "result": [
    "string"
  ]
}
```

### /get_topic_info
This function will return a few interesting statistics for a given topic. These statistics are the count
(Number of documents that are within the given topic cluster) and relevant words (these words indicate what the most common subject might be within the topic cluster, these are found using tf_idf)

Example return schema
```
{
  "result": {
    "topic_id": 0,
    "count": 0,
    "relevant_words": [
      {
        "word": "string",
        "score": 0
      }
    ]
  }
}
```

BERTopic api by ML2Grow
