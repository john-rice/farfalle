# Some of the code here is based on github.com/cohere-ai/cohere-toolkit/

from typing import Union, List
from pydantic import BaseModel, Field
from enum import Enum
from logfire.integrations.pydantic import PluginSettings


record_all = PluginSettings(logfire={"record": "all"})


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    content: str
    role: MessageRole


class ChatRequest(BaseModel):
    query: str
    history: List[Message] = Field(default_factory=list)


class RelatedQueries(BaseModel):
    related_queries: List[str] = Field(..., min_length=3, max_length=3)


class SearchResult(BaseModel):
    title: str
    url: str
    content: str

    def __str__(self):
        return f"Title: {self.title}\nURL: {self.url}\Summary: {self.content}"


class StreamEvent(str, Enum):
    SEARCH_QUERY = "search-query"
    SEARCH_RESULTS = "search-results"
    TEXT_CHUNK = "text-chunk"
    RELATED_QUERIES = "related-queries"
    STREAM_END = "stream-end"
    FINAL_RESPONSE = "final-response"


class ChatObject(BaseModel):
    event_type: StreamEvent


class SearchQueryStream(ChatObject, plugin_settings=record_all):
    event_type: StreamEvent = StreamEvent.SEARCH_QUERY
    query: str


class SearchResultStream(ChatObject, plugin_settings=record_all):
    event_type: StreamEvent = StreamEvent.SEARCH_RESULTS
    results: List[SearchResult] = Field(default_factory=list)


class TextChunkStream(ChatObject):
    event_type: StreamEvent = StreamEvent.TEXT_CHUNK
    text: str


class RelatedQueriesStream(ChatObject, plugin_settings=record_all):
    event_type: StreamEvent = StreamEvent.RELATED_QUERIES
    related_queries: List[str] = Field(default_factory=list)


class StreamEndStream(ChatObject, plugin_settings=record_all):
    event_type: StreamEvent = StreamEvent.STREAM_END


class FinalResponseStream(ChatObject, plugin_settings=record_all):
    event_type: StreamEvent = StreamEvent.FINAL_RESPONSE
    message: str


class ChatResponseEvent(BaseModel):
    event: StreamEvent
    data: Union[
        SearchQueryStream,
        SearchResultStream,
        TextChunkStream,
        RelatedQueriesStream,
        StreamEndStream,
        FinalResponseStream,
    ]