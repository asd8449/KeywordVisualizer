import streamlit as st
import pandas as pd
from konlpy.tag import Okt
from lib import NaverNewsCrawler, myTextMining, STVisualizer

st.set_page_config(page_title="텍스트 분석 대시보드", layout="wide")

# session 초기화
if "df" not in st.session_state:
    st.session_state.df = None
if "data_source" not in st.session_state:
    st.session_state.data_source = None
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "news_keyword" not in st.session_state:
    st.session_state.news_keyword = "인공지능"

with st.sidebar:
    st.subheader("데이터 소스 선택")
    source_option = st.radio("다음 중 하나를 선택하세요", ("CSV 파일 업로드", "뉴스 검색"))
    st.session_state.data_source = source_option

    if source_option == "CSV 파일 업로드":
        uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
        if uploaded_file is not None:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.success(f"CSV 파일이 업로드되었습니다. 총 {len(st.session_state.df)}개의 데이터 로드됨.")
    else:
        news_keyword = st.text_input("검색할 키워드", key="news_keyword")
        news_display = st.number_input("한 번에 가져올 기사 수", min_value=1, max_value=100, value=10)
        news_total = st.number_input("전체 가져올 기사 수", min_value=news_display, max_value=500, value=30)
        if st.button("뉴스 검색"):
            with st.spinner("뉴스 검색 중..."):
                resultAll = []
                start = 1
                keyword = st.session_state.news_keyword
                while start <= news_total:
                    resultJSON = NaverNewsCrawler.searchNaverNews(keyword, start, news_display)
                    if resultJSON is None or resultJSON.get('display', 0) == 0:
                        break
                    NaverNewsCrawler.setNewsSearchResult(resultAll, resultJSON)
                    start += news_display
                if resultAll:
                    st.session_state.df = pd.DataFrame(resultAll)
                    st.success(f"뉴스 검색 완료: {len(st.session_state.df)}개의 기사가 검색되었습니다.")
                else:
                    st.error("뉴스 검색 결과가 없습니다.")

    st.markdown("---")
    st.subheader("분석 설정")
    analysis_col = st.text_input("분석할 텍스트 컬럼명", value="description")
    top_n_bar = st.slider("빈도수 그래프 - 상위 단어 수", min_value=5, max_value=50, value=20)
    top_n_wc = st.slider("워드클라우드 - 상위 단어 수", min_value=20, max_value=200, value=50)

    show_bar = st.checkbox("빈도수 그래프 출력", value=True)
    show_wordcloud = st.checkbox("워드클라우드 출력", value=True)
    analyze_button = st.button("분석 및 시각화 실행")

st.title("텍스트 분석 결과")
preview_container = st.empty()

if st.session_state.df is not None:
    if st.session_state.data_source == "뉴스 검색":
        csv = st.session_state.df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="CSV 파일 다운로드",
            data=csv,
            file_name=f"{st.session_state.news_keyword}_naver_news.csv",
            mime="text/csv"
        )
    
    if not st.session_state.analysis_done:
        preview_container.subheader("데이터 미리보기")
        preview_container.dataframe(st.session_state.df.head(5))
    
    if analysis_col not in st.session_state.df.columns:
        st.error(f"선택한 컬럼 '{analysis_col}'이 데이터에 존재하지 않습니다. 컬럼 목록: {st.session_state.df.columns.tolist()}")
    else:
        if analyze_button:
            with st.spinner("텍스트 분석 중..."):
                corpus_list = st.session_state.df[analysis_col].dropna().astype(str).tolist()
                okt = Okt()
                tags = ['Noun', 'Adjective', 'Verb']
                stopwords = ['하며', '입', '하고', '로써', '하게', '하여', '한다', '등', '해', '이', '할', '를', '것', '전', '중', '하는', '있는', '생', '총', '했다', '의', '은', '모든', '한다고', '앞서', '는', '가', '개', '날', '론', '주', '부', '약', '폭', '가장', '주요', '있다']
                counter = myTextMining.analyze_word_freq(corpus_list, okt.pos, tags, stopwords)
                fig_bar = None
                fig_wc = None
                if show_bar:
                    fig_bar = STVisualizer.visualize_bar_chart(counter, top_n=top_n_bar,
                                                                title="단어 빈도수 그래프", xlabel="빈도", ylabel="단어")
                if show_wordcloud:
                    fig_wc = STVisualizer.visualize_wordcloud(counter, top_n=top_n_wc)
            preview_container.empty()
            st.session_state.analysis_done = True
            if fig_bar is not None:
                st.pyplot(fig_bar, use_container_width=True)
            if fig_wc is not None:
                st.pyplot(fig_wc, use_container_width=True)
            st.success("분석 및 시각화가 완료되었습니다.")
else:
    st.info("먼저 CSV 파일 업로드 또는 뉴스 검색을 통해 데이터를 확보하세요.")
