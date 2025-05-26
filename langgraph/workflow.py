"""
LangGraph workflow definition
"""
from langgraph.graph import StateGraph, END
from .state import SearchState
from .nodes import search_database, crawl_web, process_results, should_search_web


def create_search_workflow():
    """Create the search workflow"""
    workflow = StateGraph(SearchState)
    
    # Add nodes
    workflow.add_node("search_db", search_database)
    workflow.add_node("crawl_web", crawl_web)
    workflow.add_node("process", process_results)
    
    # Set edges
    workflow.set_entry_point("search_db")
    workflow.add_conditional_edges(
        "search_db",
        should_search_web,
        {
            "crawl": "crawl_web",
            "process": "process"
        }
    )
    workflow.add_edge("crawl_web", "process")
    workflow.add_edge("process", END)
    
    return workflow.compile()
