# 웹 스크래핑한 것 가사 전부 하나의 텍스트파일로 저장

import pandas as pd

# 파일 목록
file_names = ["song2020.csv", "song2021.csv", "song2022.csv", "song2023.csv"]

# 각 파일에서 'lyric' 컬럼만 추출하여 하나의 데이터프레임으로 합치기
all_lyrics = pd.DataFrame()

for file_name in file_names:
    df = pd.read_csv(file_name, usecols=["lyric"])
    all_lyrics = pd.concat([all_lyrics, df], ignore_index=True)

# 저장
all_lyrics.to_csv("all_lyrics.txt", index=False, header=False)