# Keyword Visualizer App

**Keyword Visualizer App**는 한글 키워드를 기반으로 네이버 뉴스 검색을 통해 데이터를 수집하고, 수집한 뉴스 데이터를 KoNLPy를 이용하여 텍스트 분석 후  
고빈도 단어를 이용한 **수평 막대 그래프**와 **워드클라우드**를 시각화하는 애플리케이션입니다.  
콘솔 기반 애플리케이션과 Streamlit 대시보드를 통해 데이터를 검증하고, 분석 결과를 시각적으로 확인할 수 있습니다.

---

## 주요 기능

- **키워드 기반 네이버 뉴스 검색**  
  - 한글 키워드를 입력하여 뉴스 기사를 검색합니다.  
  - 검색 결과를 CSV 파일로 다운로드 받을 수 있습니다.
  
- **텍스트 분석 및 시각화**  
  - CSV 파일 또는 뉴스 검색 결과 중 선택하여 분석할 텍스트 컬럼을 지정합니다.
  - KoNLPy를 사용한 토큰화 및 단어 빈도수 계산을 수행합니다.
  - 선택한 상위 단어 개수에 따라 **수평 막대 그래프**와 **워드클라우드**를 생성합니다.
  - 분석 결과는 사용자가 체크박스로 개별 선택하여 동시에 표시할 수 있습니다.

---

## 파일 구조

KeywordVisualizerApp/ ├── data/ # CSV 파일 저장 및 데이터 로드 폴더 ├── lib/
│ ├── myTextMining.py # 텍스트 전처리, 토큰화, 단어 빈도수 분석, 간단한 시각화 함수 포함 │ ├── NaverNewsCrawler.py # 네이버 뉴스 검색 API 호출 및 결과 CSV 저장 함수 포함 │ └── STVisualizer.py # Matplotlib을 활용한 수평 막대 그래프, 워드클라우드 시각화 함수 포함 ├── KeywordVisualizeConsoleApp.py # 콘솔(터미널) 환경에서 뉴스 검색 및 텍스트 분석 실행 └── KeywordVisualizerSTApp.py # Streamlit 기반 웹 대시보드

yaml
복사

---

## 설치 방법

1. **파이썬 및 가상 환경 설정**  
   Python 3.7 이상을 사용하는 가상 환경을 생성하세요.

2. **필수 패키지 설치**  
   다음 명령어를 사용하여 필요한 패키지를 설치합니다.
   
   ```bash
   pip install streamlit pandas konlpy wordcloud matplotlib
참고: KoNLPy 사용 시 Java(JDK) 환경이 필요합니다. KoNLPy 설치 가이드를 참고하세요.

네이버 뉴스 API 인증 정보 설정
lib/NaverNewsCrawler.py 파일 내에 있는 client_id와 client_secret 값을 네이버 개발자 센터에서 발급받은 값으로 수정하세요.

python
복사
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
실행 방법
1. 콘솔 애플리케이션
콘솔(터미널)에서 다음 명령어를 실행하면, 키워드 및 기타 옵션을 인자로 하여 뉴스 검색 후 텍스트 분석 및 시각화가 진행됩니다.

bash
복사
python KeywordVisualizeConsoleApp.py --keyword "인공지능" --csv --col "description" --display 10 --total 30
--keyword: 검색할 키워드

--csv: CSV 파일로 결과 저장 여부

--col: 분석할 텍스트 컬럼 (예: "description", "title")

--display 및 --total: 검색 결과 개수 설정

2. Streamlit 대시보드
Streamlit을 사용하여 웹 대시보드로 실행할 경우, 아래 명령어를 입력합니다.

bash
복사
streamlit run KeywordVisualizerSTApp.py
좌측 사이드바에서 데이터 소스(뉴스 검색 또는 CSV 파일 업로드)와 분석 옵션(텍스트 컬럼, 상위 단어 수, 시각화 체크박스 등)을 설정할 수 있습니다.

뉴스 검색 시, CSV 파일 다운로드 버튼을 통해 검색 결과를 파일로 저장할 수 있습니다.

분석 결과로 수평 막대 그래프와 워드클라우드를 선택적으로 출력할 수 있습니다.

참고 사항
데이터 전처리:
불용어 목록 및 분석 품사(tags)는 필요에 따라 조정할 수 있습니다.

폰트 설정:
Windows 환경에서는 c:/Windows/Fonts/malgun.ttf 폰트를 사용하지만, 환경에 따라 폰트 경로를 수정해야 할 수 있습니다.

디버깅:
Streamlit 대시보드에서 문제가 발생할 경우, 콘솔 또는 Streamlit 로그를 확인해 주세요.

License
이 프로젝트는 MIT License 하에 배포됩니다.

Contact
프로젝트에 대한 문의나 제안은 GitHub Issues를 통해 남겨주세요.

yaml
복사

---

위 내용을 그대로 복사해서 README.md 파일에 붙여넣으시면 됩니다. 프로젝트 환경에 따라 일부 내용을 조정할 수 있습니다.
