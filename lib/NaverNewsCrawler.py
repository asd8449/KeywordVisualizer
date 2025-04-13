import urllib.request
from collections import Counter
import json

def searchNaverNews(keyword, start, display):
    client_id = "1RyZqJxbt9OOw4pakFEk"
    client_secret = "co9HDKypXO"
    
    encText = urllib.parse.quote(keyword)
    url = "https://openapi.naver.com/v1/search/news?query=" + encText
    
    new_url = url + f'&start={start}&display={display}'
    request = urllib.request.Request(new_url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    resultJSON = None
    try:
        response = urllib.request.urlopen(request)
        
        rescode = response.getcode()
        if(rescode == 200):
            response_body = response.read()
            resultJSON = json.loads(response_body.decode('utf-8'))
        else:
            print("Error Code:" + rescode)
    except Exception as e:
        print(e)
        print(f'Error : {new_url}')

    return resultJSON

def setNewsSearchResult(resultAll, resultJSON):
    for result in resultJSON['items']:
        resultAll.append(result)

def saveSearchResult_CSV(json_list, filename):
    import pandas as pd
    data_df = pd.DataFrame(json_list)
    data_df.to_csv(filename)
    print(f'{filename} SAVED')

def visuallize_wordcloud(counter, keyword):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    font_path = "c:/Windows/fonts/malgun.ttf"

    wordcloud = WordCloud(font_path, width=600, height=600, max_words=20, background_color='ivory')

    wordcloud = wordcloud.generate_from_frequencies(counter)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

    output_filename = './result/' + f'{keyword}_wordcloud.png'
    wordcloud.to_file(output_filename)

def load_corpus_from_csv(corpus_file, col_name):
    import pandas as pd
    data_df = pd.read_csv(corpus_file)
    result_list = list(data_df[col_name])
    return result_list

def analyze_word_freq(corpus_list, tokenizer, tags, stopwords):
    token_list = tokenize_korean_corpus(corpus_list, tokenizer, tags, stopwords)
    
    counter = Counter(token_list)
    return counter

def tokenize_korean_corpus(corpus_list, tokenizer, tags, stopwords):
    text_pos_list = []
    for text in corpus_list:
        text_pos = tokenizer(text)
        text_pos_list.extend(text_pos)
    token_list = [token for token, tag in text_pos_list if tag in tags and token not in stopwords]
    return token_list
