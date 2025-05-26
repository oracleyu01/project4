"""
LangGraph node functions
"""
import time
from langchain_core.messages import HumanMessage, AIMessage
from .state import SearchState
from database import SupabaseClient
from crawlers import ProConsLaptopCrawler


# Initialize clients
supabase_client = SupabaseClient()
crawler = ProConsLaptopCrawler()


def search_database(state: SearchState) -> SearchState:
    """Search product in database"""
    product_name = state["product_name"]
    
    state["messages"].append(
        HumanMessage(content=f"Searching database for: {product_name}")
    )
    
    try:
        # Try exact match first
        exact_match = supabase_client.search_exact(product_name)
        if exact_match.data:
            state["search_method"] = "database"
            state["results"] = {"data": exact_match.data}
            state["messages"].append(
                AIMessage(content=f"Found {len(exact_match.data)} results in database")
            )
            return state
        
        # Try partial match
        partial_match = supabase_client.search_partial(product_name)
        if partial_match.data:
            state["search_method"] = "database"
            state["results"] = {"data": partial_match.data}
            state["messages"].append(
                AIMessage(content=f"Found {len(partial_match.data)} partial matches in database")
            )
            return state
        
        # Try similarity search
        state["messages"].append(
            AIMessage(content="No exact match found, trying similarity search...")
        )
        similar_match = supabase_client.search_similar(product_name, threshold=0.7)
        if similar_match and similar_match.data:
            state["search_method"] = "similarity"
            state["results"] = {"data": similar_match.data}
            state["messages"].append(
                AIMessage(content=f"Found similar product in database using AI similarity")
            )
            return state
        
        state["messages"].append(
            AIMessage(content="No results found in database, will search web")
        )
        state["results"] = {"data": None}
        return state
        
    except Exception as e:
        state["error"] = str(e)
        state["messages"].append(
            AIMessage(content=f"Database search error: {str(e)}")
        )
        return state


def crawl_web(state: SearchState) -> SearchState:
    """Crawl web for product information"""
    if state["results"].get("data"):  # Already found in DB
        return state
    
    product_name = state["product_name"]
    state["search_method"] = "web_crawling"
    
    state["messages"].append(
        HumanMessage(content=f"Starting web crawl for: {product_name}")
    )
    
    all_pros = []
    all_cons = []
    sources = []
    
    # Search queries
    search_queries = [
        f"{product_name} 장단점 실사용",
        f"{product_name} 후기"
    ]
    
    for query in search_queries[:2]:
        state["messages"].append(
            AIMessage(content=f"Searching Naver for: {query}")
        )
        
        result = crawler.search_blog(query, display=5)
        if not result or 'items' not in result:
            continue
        
        posts = result['items']
        
        for idx, post in enumerate(posts[:3]):
            state["messages"].append(
                AIMessage(content=f"Crawling blog post: {post['title'][:50]}...")
            )
            
            content = crawler.crawl_content(post['link'])
            if not content:
                continue
            
            pros_cons = crawler.extract_pros_cons_with_gpt(product_name, content)
            
            if pros_cons:
                all_pros.extend(pros_cons['pros'])
                all_cons.extend(pros_cons['cons'])
                sources.append({
                    'title': post['title'],
                    'link': post['link']
                })
                
                state["messages"].append(
                    AIMessage(content=f"Extracted {len(pros_cons['pros'])} pros and {len(pros_cons['cons'])} cons")
                )
            
            time.sleep(0.5)
    
    # Remove duplicates
    state["pros"] = list(dict.fromkeys(all_pros))[:10]
    state["cons"] = list(dict.fromkeys(all_cons))[:10]
    state["sources"] = sources[:5]
    
    # Save to database with embeddings if we found data
    if state["pros"] or state["cons"]:
        state["messages"].append(
            AIMessage(content="Saving results to database with embeddings...")
        )
        supabase_client.insert_pros_cons_with_embedding(
            product_name, 
            state["pros"], 
            state["cons"]
        )
    
    state["messages"].append(
        AIMessage(content=f"Web crawl complete. Found {len(state['pros'])} pros and {len(state['cons'])} cons")
    )
    
    return state


def process_results(state: SearchState) -> SearchState:
    """Process and organize results"""
    if state["search_method"] in ["database", "similarity"] and state["results"].get("data"):
        # Process DB results
        data = state["results"]["data"]
        state["pros"] = [item['content'] for item in data if item['type'] == 'pro']
        state["cons"] = [item['content'] for item in data if item['type'] == 'con']
        state["sources"] = []  # No sources for DB results
        
        state["messages"].append(
            AIMessage(content=f"Processed results: {len(state['pros'])} pros, {len(state['cons'])} cons")
        )
    
    return state


def should_search_web(state: SearchState) -> str:
    """Determine if web search is needed"""
    if state["results"].get("data"):
        return "process"
    else:
        return "crawl"
