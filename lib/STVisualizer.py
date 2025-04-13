# lib/STVisualizer.py
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from wordcloud import WordCloud

def visualize_bar_chart(counter, top_n=20, title="Bar Chart", xlabel="Frequency", ylabel="Words"):
    common_words = counter.most_common(top_n)
    words = [word for word, count in common_words]
    counts = [count for word, count in common_words]
    
    # 한글 폰트 설정 (환경에 맞게 경로 수정)
    font_path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(words[::-1], counts[::-1])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    return fig

def visualize_wordcloud(counter, top_n=100):
    freq_dict = dict(counter.most_common(top_n))
    
    font_path = "c:/Windows/Fonts/malgun.ttf"
    wc = WordCloud(font_path=font_path, width=800, height=600, background_color='ivory')
    wc.generate_from_frequencies(freq_dict)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    plt.tight_layout()
    return fig
