"""
Smart Shopping App - Main Streamlit Application with OpenAI Embeddings
"""
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage

# Import custom modules
from config import settings
from langgraph import create_search_workflow
from utils import CSS_STYLES, HEADER_HTML, PROS_SECTION_HTML, CONS_SECTION_HTML

# Page configuration
st.set_page_config(
    page_title="스마트한 쇼핑",
    page_icon="🛒",
    layout="wide"
)

# Apply CSS styles
st.markdown(CSS_STYLES, unsafe_allow_html=True)

# Display header
st.markdown(HEADER_HTML, unsafe_allow_html=True)

# Initialize workflow
@st.cache_resource
def get_search_workflow():
    return create_search_workflow()

search_app = get_search_workflow()

# Search section
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    product_name = st.text_input(
        "🔍 제품명을 입력하세요",
        placeholder="예: 맥북 프로 M3, LG 그램 2024, 갤럭시북4 프로"
    )
    
    search_button = st.button("검색하기", use_container_width=True)

# Execute search
if search_button and product_name:
    with st.spinner(f"'{product_name}' 검색 중..."):
        # Initialize state
        initial_state = {
            "product_name": product_name,
            "search_method": "",
            "results": {},
            "pros": [],
            "cons": [],
            "sources": [],
            "messages": [],
            "error": "",
            "similar_products": []
        }
        
        # Run workflow
        final_state = search_app.invoke(initial_state)
    
    # Display results
    if final_state["pros"] or final_state["cons"]:
        # Show search method
        if final_state["search_method"] == "database":
            st.success(f"✅ 데이터베이스에서 '{product_name}' 정보를 찾았습니다!")
        elif final_state["search_method"] == "similarity":
            st.info(f"🤖 AI 유사도 검색으로 관련 제품 정보를 찾았습니다!")
        else:
            st.warning(f"🔄 웹에서 '{product_name}' 정보를 실시간으로 수집했습니다!")
        
        # Display pros and cons
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(PROS_SECTION_HTML, unsafe_allow_html=True)
            for idx, pro in enumerate(final_state["pros"][:10], 1):
                st.write(f"{idx}. {pro}")
        
        with col2:
            st.markdown(CONS_SECTION_HTML, unsafe_allow_html=True)
            for idx, con in enumerate(final_state["cons"][:10], 1):
                st.write(f"{idx}. {con}")
        
        # Statistics
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("총 장점", f"{len(final_state['pros'])}개")
        with col2:
            st.metric("총 단점", f"{len(final_state['cons'])}개")
        with col3:
            method_display = {
                "database": "DB (정확히 일치)",
                "similarity": "AI 유사도 검색",
                "web_crawling": "웹 크롤링"
            }
            st.metric("검색 방법", method_display.get(final_state["search_method"], "웹"))
        
        # Sources (for web crawling)
        if final_state["sources"]:
            with st.expander("📚 출처 보기"):
                for idx, source in enumerate(final_state["sources"], 1):
                    st.write(f"{idx}. [{source['title']}]({source['link']})")
        
        # LangGraph execution log
        with st.expander("🔍 검색 프로세스 (LangSmith에서 확인 가능)"):
            for msg in final_state["messages"]:
                if isinstance(msg, HumanMessage):
                    st.write(f"👤 {msg.content}")
                else:
                    st.write(f"🤖 {msg.content}")
    else:
        st.error(f"'{product_name}'에 대한 정보를 찾을 수 없습니다.")

# Footer information
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("💡 검색 프로세스는 LangSmith에서 상세히 확인할 수 있습니다.")
with col2:
    st.info("🤖 OpenAI 임베딩을 사용하여 유사한 제품도 찾아드립니다.")

current_date = datetime.now().strftime('%Y년 %m월 %d일')
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>마지막 업데이트: {current_date}</p>
    <p>Powered by OpenAI Embeddings & LangGraph</p>
</div>
""", unsafe_allow_html=True)
