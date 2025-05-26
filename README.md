# 🛒 스마트한 쇼핑 앱 (Smart Shopping App)

LangGraph를 활용한 제품 리뷰 장단점 분석 애플리케이션

## 📋 개요

이 애플리케이션은 사용자가 입력한 제품명에 대해 실제 사용자들의 블로그 리뷰를 수집하고 분석하여 장점과 단점을 한눈에 볼 수 있도록 제공합니다.

### 주요 기능

- **데이터베이스 우선 검색**: Supabase에 저장된 기존 리뷰 데이터 활용
- **실시간 웹 크롤링**: 데이터베이스에 없는 제품은 네이버 블로그에서 실시간 수집
- **AI 기반 분석**: GPT를 활용한 장단점 자동 추출
- **LangGraph 워크플로우**: 체계적인 검색 프로세스 관리
- **LangSmith 연동**: 실행 과정 추적 및 디버깅 (선택사항)

## 🚀 시작하기

### 사전 요구사항

- Python 3.8 이상
- Supabase 계정 및 프로젝트
- OpenAI API 키
- 네이버 개발자 API 키 (블로그 검색용)
- (선택) LangSmith API 키

### 설치

1. 저장소 클론
```bash
git clone https://github.com/yourusername/smart-shopping-app.git
cd smart-shopping-app
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
```bash
cp .env.example .env
```

`.env` 파일을 열어 필요한 API 키들을 입력합니다:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_api_key
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret
LANGSMITH_API_KEY=your_langsmith_api_key  # 선택사항
```

### Supabase 테이블 설정

Supabase에 다음 구조의 테이블을 생성합니다:

```sql
CREATE TABLE laptop_pros_cons (
    id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('pro', 'con')),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_product_name ON laptop_pros_cons(product_name);
```

### 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속합니다.

## 📁 프로젝트 구조

```
smart-shopping-app/
│
├── app.py                    # Streamlit 메인 애플리케이션
├── requirements.txt          # 의존성 목록
├── .env.example             # 환경 변수 예시
├── .gitignore              # Git 제외 파일
│
├── config/                  # 설정 관련
│   ├── __init__.py
│   └── settings.py         # 환경 설정
│
├── crawlers/               # 크롤링 관련
│   ├── __init__.py
│   └── naver_crawler.py   # 네이버 블로그 크롤러
│
├── database/              # 데이터베이스 관련
│   ├── __init__.py
│   └── supabase_client.py # Supabase 클라이언트
│
├── langgraph/            # LangGraph 관련
│   ├── __init__.py
│   ├── state.py         # 상태 정의
│   ├── nodes.py         # 노드 함수
│   └── workflow.py      # 워크플로우 정의
│
└── utils/               # 유틸리티
    ├── __init__.py
    └── styles.py       # CSS 스타일
```

## 🔄 워크플로우

1. **데이터베이스 검색**: 입력된 제품명으로 Supabase 검색
2. **조건부 분기**: 
   - 데이터 존재 시 → 결과 처리
   - 데이터 없을 시 → 웹 크롤링
3. **웹 크롤링**: 네이버 블로그 검색 및 내용 수집
4. **AI 분석**: GPT를 통한 장단점 추출
5. **결과 표시**: 장단점 및 출처 정보 표시

## 🛠 기술 스택

- **Frontend**: Streamlit
- **Workflow**: LangGraph
- **Database**: Supabase
- **AI/ML**: OpenAI GPT, Sentence Transformers
- **Web Scraping**: BeautifulSoup4, Requests
- **Monitoring**: LangSmith (선택사항)

## 📝 사용 예시

1. 제품명 입력: "맥북 프로 M3", "LG 그램 2024" 등
2. 검색 버튼 클릭
3. 결과 확인:
   - 장점/단점 목록
   - 검색 방법 (DB/웹)
   - 출처 정보 (웹 크롤링의 경우)

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 🙏 감사의 말

- Anthropic의 LangGraph 팀
- Streamlit 커뮤니티
- OpenAI
- Naver Developers
