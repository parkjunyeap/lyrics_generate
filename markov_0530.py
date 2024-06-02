# 마르코프 체인 딕셔너리만들고 , 시작단어 시 단어 생성

import os
import json
import random
from konlpy.tag import Okt

# 마르코프 체인 딕셔너리 만들기 --- (※1)
def make_dic(words):
    tmp = ["@"]
    dic = {}
    for word in words:
        tmp.append(word)
        if len(tmp) < 3: continue
        if len(tmp) > 3: tmp = tmp[1:]
        set_word3(dic, tmp)
        if word == ".":
            tmp = ["@"]
            continue
    return dic

# 딕셔너리에 데이터 등록하기 --- (※2)
def set_word3(dic, s3):
    w1, w2, w3 = s3
    if not w1 in dic: dic[w1] = {}
    if not w2 in dic[w1]: dic[w1][w2] = {}
    if not w3 in dic[w1][w2]: dic[w1][w2][w3] = 0
    dic[w1][w2][w3] += 1

# 단어 선택 함수
def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))

# 주어진 단어로 시작하는 지정된 길이의 문장 만들기 --- (※3)
def make_sentence(dic, start_word, length=8):
    if start_word not in dic: return "해당 단어는 사전에 없습니다."
    ret = [start_word]
    w1 = start_word
    if w1 not in dic: return "해당 단어는 사전에 없습니다."
    w2 = word_choice(dic[w1])
    ret.append(w2)
    for _ in range(length - 2):  # 시작 단어와 두 번째 단어를 이미 추가했으므로 length-2번 반복
        if w1 not in dic or w2 not in dic[w1]: break
        w3 = word_choice(dic[w1][w2])
        ret.append(w3)
        w1, w2 = w2, w3
    return ret

# 문장 읽어 들이기 --- (※4)
lyrics_file = "all_lyrics.txt"
dict_file = "markov-lyrics2.json"
if not os.path.exists(dict_file):
    # 가사 텍스트 파일 읽어 들이기
    with open(lyrics_file, "r", encoding="utf-8") as f:
        text = f.read()
    text = text.replace("…", "")  # 현재 koNLPy가 …을 구두점으로 잡지 못하는 문제 임시 해결
    # 형태소 분석
    okt = Okt()
    malist = okt.pos(text, norm=True)
    words = []
    for word in malist:
        # 구두점 등은 대상에서 제외(단 마침표는 포함)
        if not word[1] in ["Punctuation"]:
            words.append(word[0])
        if word[0] == ".":
            words.append(word[0])
    # 딕셔너리 생성
    dic = make_dic(words)
    json.dump(dic, open(dict_file, "w", encoding="utf-8"), ensure_ascii=False)
else:
    dic = json.load(open(dict_file, "r", encoding="utf-8"))

# 주어진 단어로 시작하는 문장 만들기 --- (※5)
start_word = input("시작 단어를 입력하세요: ")
all_sentences = []
for i in range(40):
    sentence = make_sentence(dic, start_word, length=8)
    if isinstance(sentence, str):  # "해당 단어는 사전에 없습니다."와 같은 오류 메시지 처리
        print(sentence)
        break
    all_sentences.append(" ".join(sentence))
    start_word = sentence[-1]  # 다음 문장은 이전 문장의 마지막 단어로 시작

# 40줄 출력
for line in all_sentences:
    print(line)