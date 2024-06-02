# 여기서 워드클라우드 2020~2023 출력

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import re
from collections import Counter
from nltk.tokenize import word_tokenize
import nltk
from konlpy.tag import Okt
import requests
import numpy as np

# NLTK 리소스 다운로드 (필요시 주석 해제)
# nltk.download('punkt')
# nltk.download('stopwords')

# 한국어 불용어 목록 다운로드
url = 'https://raw.githubusercontent.com/stopwords-iso/stopwords-ko/master/stopwords-ko.txt'
response = requests.get(url)
korean_stopwords = response.text.split('\n')

# 영어 불용어 목록 설정
from nltk.corpus import stopwords
english_stopwords = set(stopwords.words('english'))

# 한국어 분석을 위한 객체 생성
okt = Okt()

def generate_wordclouds(file_path):
    # CSV 파일 로드
    df = pd.read_csv(file_path)
    lyrics = df['lyric']
    all_lyrics = ' '.join(lyrics.tolist())

    # 영어와 한국어 분리
    english_lyrics = re.sub(r'[^a-zA-Z\s]', '', all_lyrics)
    korean_lyrics = re.sub(r'[a-zA-Z0-9]', '', all_lyrics)
    # 영어 토큰화 및 불용어 제거
    english_tokens = [word for word in word_tokenize(english_lyrics.lower()) if word not in english_stopwords and len(word) > 1]

    # 한국어 토큰화 및 명사 추출, 불용어 제거
    korean_tokens = [word for word in okt.nouns(korean_lyrics) if word not in korean_stopwords and len(word) > 1]

    # 단어 빈도 분석
    english_counter = Counter(english_tokens)
    korean_counter = Counter(korean_tokens)

    # WordCloud 생성
    english_wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(english_counter)
    korean_wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=r'C:\Users\bab85\OneDrive\바탕 화면\자연어처리\nanum-barun-gothic\NanumBarunGothic.ttf').generate_from_frequencies(korean_counter)

    return english_wordcloud, korean_wordcloud, english_tokens, korean_tokens

# 마르코프 체인을 위한 단어 사전 구축 함수
def build_markov_chain(text_tokens):
    markov_chain = {}
    for i in range(len(text_tokens)-1):
        word = text_tokens[i]
        next_word = text_tokens[i+1]
        if word not in markov_chain:
            markov_chain[word] = {}
        if next_word not in markov_chain[word]:
            markov_chain[word][next_word] = 0
        markov_chain[word][next_word] += 1
    return markov_chain

# 주어진 단어로부터 가사 생성
def generate_lyrics(markov_chain, start_word, length=50):
    word = start_word
    lyrics = [word]
    for i in range(length-1):
        if word not in markov_chain or not markov_chain[word]:
            break
        next_words = list(markov_chain[word].keys())
        word_weights = list(markov_chain[word].values())
        word = np.random.choice(next_words, p=np.array(word_weights) / sum(word_weights))
        lyrics.append(word)
    return ' '.join(lyrics)

# 전체 가사에서 가장 많이 사용된 단어와 그 다음 단어 추출
def most_common_words(text_tokens):
    counter = Counter(text_tokens)
    most_common_word = counter.most_common(1)[0][0]
    next_words = [text_tokens[i+1] for i in range(len(text_tokens)-1) if text_tokens[i] == most_common_word]
    next_word_counter = Counter(next_words)
    next_most_common_word = next_word_counter.most_common(1)[0][0]
    return most_common_word, next_most_common_word


# 연도별 CSV 파일 경로
years = [2020, 2021, 2022, 2023]
file_paths = [f'song{year}.csv' for year in years]

for file_path in file_paths:
    # 단어 구름 생성 및 토큰 반환
    english_wordcloud, korean_wordcloud, english_tokens, korean_tokens = generate_wordclouds(file_path)
    
    # 단어 구름 시각화
    plt.figure(figsize=(15, 7))
    plt.subplot(1, 2, 1)
    plt.imshow(english_wordcloud, interpolation='bilinear')
    plt.axis('off')
    year = file_path.split('song')[-1].split('.')[0]  # 파일 경로에서 연도 추출
    plt.title(f'English WordCloud - {year}')

    plt.subplot(1, 2, 2)
    plt.imshow(korean_wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Korean WordCloud - {year}')

    plt.show()

