# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import os
import json
import random
from konlpy.tag import Okt
import re
from pykospacing import Spacing

app = Flask(__name__)

spacing = Spacing()

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

def set_word3(dic, s3):
    w1, w2, w3 = s3
    if not w1 in dic: dic[w1] = {}
    if not w2 in dic[w1]: dic[w1][w2] = {}
    if not w3 in dic[w1][w2]: dic[w1][w2][w3] = 0
    dic[w1][w2][w3] += 1

def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))

def make_sentence(dic, start_word, length=8): 
    if start_word not in dic: return "해당 단어는 사전에 없습니다."
    ret = [start_word]
    w1 = start_word
    if w1 not in dic: return "해당 단어는 사전에 없습니다."
    w2 = word_choice(dic[w1])
    ret.append(w2)
    for _ in range(length - 2):
        if w1 not in dic or w2 not in dic[w1]: break
        w3 = word_choice(dic[w1][w2])
        ret.append(w3)
        w1, w2 = w2, w3
    return ret

def split_korean_english(text):
    korean = re.findall(r'[\u3131-\uD79D]+', text)
    english = re.findall(r'[a-zA-Z]+', text)
    return korean, english

lyrics_file = "static/all_lyrics.txt"
dict_file = "static/markov-lyrics2.json"
if not os.path.exists(dict_file):
    with open(lyrics_file, "r", encoding="utf-8") as f:
        text = f.read()
    text = text.replace("…", "")
    okt = Okt()
    malist = okt.pos(text, norm=True)
    words = []
    for word in malist:
        if not word[1] in ["Punctuation"]:
            words.append(word[0])
        if word[0] == ".":
            words.append(word[0])
    dic = make_dic(words)
    json.dump(dic, open(dict_file, "w", encoding="utf-8"), ensure_ascii=False)
else:
    dic = json.load(open(dict_file, "r", encoding="utf-8"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    start_word = request.json.get('start_word')
    all_sentences = []
    for i in range(40):
        sentence = make_sentence(dic, start_word, length=8)
        if isinstance(sentence, str):
            return jsonify({'error': sentence})
        if i > 0:
            sentence = sentence[1:]
        all_sentences.append(" ".join(sentence))
        start_word = sentence[-1]
    
    corrected_sentences = []
    for line in all_sentences:
        korean, english = split_korean_english(line)
        korean_text_no_spaces = ''.join(korean).replace(" ", "")
        corrected_korean = spacing(korean_text_no_spaces)
        corrected_text = corrected_korean + ' ' + ' '.join(english)
        corrected_sentences.append(corrected_text)

    return jsonify({'lyrics': "\n".join(corrected_sentences)})

if __name__ == '__main__':
    app.run(debug=True)
