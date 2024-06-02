from pykospacing import Spacing
spacing = Spacing()
print(spacing("이런 말놀랐다면 미안해 부담이"))
# "김형호 영화시장 분석가는 '1987'의 네이버 영화 정보 네티즌 10점 평에서 언급된 단어들을 지난해 12월 27일부터 올해 1월 10일까지 통계 프로그램 R과 KoNLP 패키지로 텍스트마이닝하여 분석했다.")
# Apply a list of words that must be non-spacing
print(spacing('귀밑에서턱까지잇따라난수염을구레나룻이라고한다.'))
# '귀 밑에서 턱까지 잇따라 난 수염을 구레나 룻이라고 한다.'
print(spacing = Spacing(rules=['구레나룻']))
print(spacing('귀밑에서턱까지잇따라난수염을구레나룻이라고한다.'))


# '귀 밑에서 턱까지 잇따라 난 수염을 구레나룻이라고 한다.'