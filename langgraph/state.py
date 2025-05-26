"""
LangGraph state definitions
"""
from typing import TypedDict, Annotated, List, Union
from langchain_core.messages import HumanMessage, AIMessage
import operator


class SearchState(TypedDict):
    """State for the search process"""
    product_name: str
    search_method: str  # "database" or "web_crawling"
    results: dict
    pros: List[str]
    cons: List[str]
    sources: List[dict]
    messages: Annotated[List[Union[HumanMessage, AIMessage]], operator.add]
    error: str
