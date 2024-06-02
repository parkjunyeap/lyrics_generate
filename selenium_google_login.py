# pip install selenium
# pip install chromedriver-autoinstaller

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
import subprocess
import time

# Chrome 드라이버 자동 설치 및 버전 확인
chromedriver_autoinstaller.install()

# Chrome 드라이버 서비스 설정
s = Service(chromedriver_autoinstaller.install())

# Google Chrome을 디버깅 모드로 열기 위한 설정
subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') 

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Chrome 드라이버 설정
try:
    driver = webdriver.Chrome(service=s, options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(service=s, options=option)
    
driver.implicitly_wait(10) 

# suno.com 페이지로 이동
driver.get('https://suno.com/')

# 잠시 대기 (페이지 로드 대기)
time.sleep(3)

# 'Create' 버튼 클릭 (지정된 요소를 찾아 클릭)
create_button = driver.find_element(By.CSS_SELECTOR, 'div.css-3yc08u[data-theme="dark"]')
create_button.click()

# 잠시 대기 (페이지 로드 대기)
time.sleep(3)

# 스위치 토글 찾기 및 클릭
toggle_switch = driver.find_element(By.CSS_SELECTOR, 'span.chakra-switch__track[data-theme="dark"]')
toggle_switch.click()

# 잠시 대기 (토글 후 처리 대기)
time.sleep(1)

# 'textarea' 요소 찾기 (가사 입력란)
lyrics_textarea = driver.find_element(By.CSS_SELECTOR, 'textarea.chakra-textarea[data-testid="lyrics-textarea"]')

# 입력할 텍스트 배열 // 사용자가 입력한 거 넣어야함.
texts = ['안녕 어제의 나니까 네가 Oh', '원망스럽네요 다시금 날 봐줘요 그대의 ', '아름다운 추억이 떠오르면 많이 많이 좋아해 ', '너를 보낸 게 잘한 일이 되도록 ', '더욱 눈부시게 웃어주기를 그림처럼 ', '날 꽃 피우게 해 매일 널 꿈꾸겠지만 ', '가득 채울 순 없는 걸까 이제 넌 ', '못 감당해 날 보고 배워요 EBS', '흔들릴 바엔 그리워 아픈 게 나아 ', '서둘러 안겨본 그 품은 따스할 테 ', '고행여나 울더라도 흔들리진 말자 ', '낭만을 전파 올해 꼬였 Positive vibe', '대도 성장한 거 야 뒤돌아보면 no prob', '날 보며 웃어주던 네가 내게로 오는 ', '첫눈같이 믿기지 않는 기적 같은 ', '하늘 아래 다른 세상 속에 참 ', '뭘 그렇게 나 놀래나 더 재밌는 걸 보여줄게 ', ' When the weekend comes I can fly', '이제 조금 낯선 다른 차원 so fast', '까지 들어봐 Get loud NewJeans So', ' keep it down Blackpink in your Credit', '고마웠던 사람들 아사는 게 개 같지 ', '아발가벗겨져 버린 아별빛 Movie star', '은아뜩하니 은하수를 믿지 않아 now', '마치 달과 지구는  언제부터 ', '인지 그대를 놓친 거에요나 ', '오늘 너에게 묻는 건지 오늘 고백 ', '할 거야 작은 너를 너무 사랑 ', '했나봐 멀어지는 거지 같은 미련이 ', '있는 곳에 shine like the stars', '밤하늘에 세상이 너를 stars', '우린 어쩌다 헤어진 걸까 수없이 부른 이름 ', '어딘가에 있겠지 하며 이 밤이 ', '어가면 구름 너머 세상을 OK', '전하지 못하는 내 아버지 세상 ', '비슷한 걸 테니까 머리 위로 선선히 ', '부는 바람파도가 치거든 저파도 ', '깜깜하게 나를 스쳐도 절대 끌려가지 않을 ', '이것은 또 물보라를 secret', '기억해 이제는 나를 재촉하던 ']

# 텍스트 배열 입력
for text in texts:
    lyrics_textarea.send_keys(text + '\n')

# 'textarea' 요소 찾기 (스타일 입력란)
style_textarea = driver.find_element(By.CSS_SELECTOR, 'textarea.chakra-textarea[data-testid="style-textarea"]')
style_textarea.send_keys('시티팝')

# 'input' 요소 찾기 (제목 입력란)
title_input = driver.find_element(By.CSS_SELECTOR, 'input.chakra-input[data-testid="title-input"]')
title_input.send_keys('해성쿤잘가')

# 'Create' 버튼 클릭
create_button = driver.find_element(By.CSS_SELECTOR, 'button.chakra-button[data-testid="create-button"]')
create_button.click()

# 주기적으로 링크가 나타날 때까지 확인
link_xpath = '//a[@data-theme="dark" and text()="해성쿤잘가"]'
link_found = False
while not link_found:
    try:
        song_link = driver.find_element(By.XPATH, link_xpath)
        link_found = True
    except:
        time.sleep(1)  # 링크가 나타날 때까지 1초 간격으로 확인

# 링크 클릭
song_link.click()

# 잠시 대기 (페이지 로드 대기)
time.sleep(3)

# 재생 버튼 클릭
play_button = driver.find_element(By.CSS_SELECTOR, 'svg.chakra-icon.css-180tifu')
play_button.click()

# 잠시 대기 (재생 후 처리 대기)
time.sleep(5)

# 웹드라이버 종료
driver.quit()
