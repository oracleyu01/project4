"""
CSS styles for the Streamlit app
"""

CSS_STYLES = """
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .pros-section {
        background-color: #d4edda;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 5px solid #28a745;
    }
    .cons-section {
        background-color: #f8d7da;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 5px solid #dc3545;
    }
</style>
"""

HEADER_HTML = """
<div class="main-header">
    <h1>🛒 스마트한 쇼핑 (LangGraph)</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        블로그에서 수집한 실사용 후기를 바탕으로 제품의 장점과 단점을 한눈에 확인하세요
    </p>
</div>
"""

PROS_SECTION_HTML = """
<div class="pros-section">
    <h3>✅ 장점</h3>
</div>
"""

CONS_SECTION_HTML = """
<div class="cons-section">
    <h3>❌ 단점</h3>
</div>
"""
