# KeywordVisualizeConsoleApp.py
import os
import argparse
from lib import NaverNewsCrawler, myTextMining, STVisualizer
from konlpy.tag import Okt
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Keyword Visualize Console App")
    parser.add_argument("--keyword", type=str, required=True, help="검색할 키워드")
    parser.add_argument("--csv", action="store_true", help="CSV 저장 여부")
    parser.add_argument("--col", type=str, default="description", help="분석할 컬럼명 (예: description, title)")
    parser.add_argument("--display", type=int, default=10, help="한 번에 가져올 기사 수")
    parser.add_argument("--total", type=int, default=30, help="전체 가져올 기사 수")
    args = parser.parse_args()

    keyword = args.keyword
    csv_save = args.csv
    col_name = args.col
    display = args.display
    total = args.total

    resultAll = []
    start = 1
    while start <= total:
        resultJSON = NaverNewsCrawler.searchNaverNews(keyword, start, display)
        if resultJSON is None or resultJSON.get('display', 0) == 0:
            break
        NaverNewsCrawler.setNewsSearchResult(resultAll, resultJSON)
        print(f"{keyword} [{start}] : Search Request Success")
        start += display

    csv_filename = f"./data/{keyword}_naver_news.csv"
    os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
    NaverNewsCrawler.saveSearchResult_CSV(resultAll, csv_filename)

    corpus_list = myTextMining.load_corpus_from_csv(csv_filename, col_name)

    okt = Okt()
    tags = ['Noun', 'Adjective', 'Verb']
    stopwords = ['하며', '입', '하고', '로써', '하게', '하여', '한다']
    counter = myTextMining.analyze_word_freq(corpus_list, okt.pos, tags, stopwords)

    # 시각화
    fig_bar = STVisualizer.visualize_bar_chart(counter, top_n=20, title=f"{keyword} 뉴스 키워드 빈도수", xlabel="빈도", ylabel="단어")
    fig_wc = STVisualizer.visualize_wordcloud(counter, top_n=100)
    
    # 생성된 이미지를 저장하지 않고, 화면에 출력
    plt.show()

if __name__ == "__main__":
    main()
