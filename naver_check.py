import requests
import json
from bs4 import BeautifulSoup

# 네이버 맞춤법 검사기 함수
def check_spelling(text):
    url = "https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy"
    params = {
        "where": "nexearch",
        "query": text,
        "service": "speller",
        "color_blindness": 0
    }
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return "Error: Could not reach the API."
    
    try:
        result_json = response.json()
        result_html = result_json['message']['result']['html']
        corrected_text = BeautifulSoup(result_html, "html.parser").get_text()
    except KeyError as e:
        print("KeyError:", e)
        print("Response JSON:", result_json)
        return "Error: The structure of the response has changed."
    
    return corrected_text

# 테스트할 문장
test_text = "안녕 하세요. 저는 한국인 입니다.이문장은한글로작성됬습니다."

# 맞춤법 검사기 호출
corrected_text = check_spelling(test_text)
print("원문: ", test_text)
print("교정된 문장: ", corrected_text)
