smart-shopping-app/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── app.py                    # Streamlit 메인 앱
│
├── config/
│   └── __init__.py
│   └── settings.py          # 환경 설정
│
├── crawlers/
│   └── __init__.py
│   └── naver_crawler.py     # 네이버 블로그 크롤러
│
├── database/
│   └── __init__.py
│   └── supabase_client.py   # Supabase 클라이언트
│
├── langgraph/
│   └── __init__.py
│   └── state.py             # LangGraph 상태 정의
│   └── nodes.py             # LangGraph 노드 함수
│   └── workflow.py          # LangGraph 워크플로우
│
└── utils/
    └── __init__.py
    └── styles.py            # CSS 스타일
