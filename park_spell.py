from pykospacing import Spacing

# 초기화
spacing = Spacing()

# 입력 텍스트
text = "안 녕 하세요. 제 이 름 은 홍 길 동 입 니 다. 오늘 날 씨 가 아 주 좋 네 요."

# 모든 공백 제거
text_no_spaces = text.replace(" ", "")

# 띄어쓰기 검사
corrected_text = spacing(text_no_spaces)

print(corrected_text)