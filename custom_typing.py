from typing import List
from typing_extensions import TypedDict


class find_topic_response(TypedDict):
    class inner_find_topic_res(TypedDict):
        topic_id: int
        probability: float

    result: List[inner_find_topic_res]


class get_topics_response(TypedDict):
    class inner_get_topics_response(TypedDict):
        text: str
        topic_id: int
        probability: float

    result: List[inner_get_topics_response]


class health_response(TypedDict):
    status: str


class get_relevant_response(TypedDict):
    result: list


class get_topic_info_response(TypedDict):
    class inner_overview(TypedDict):
        class inner_get_topic_info(TypedDict):
            word: str
            score: float

        topic_id: int
        count: int
        relevant_words: List[inner_get_topic_info]

    result: inner_overview
