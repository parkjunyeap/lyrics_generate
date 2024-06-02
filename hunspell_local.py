import subprocess
import os

def check_spelling(text, dic_path, dic_name):
    # 절대 경로 생성
    abs_dic_path = os.path.abspath(dic_path)
    
    # 사전 파일 존재 여부 확인
    dic_file = os.path.join(abs_dic_path, f"{dic_name}.dic")
    aff_file = os.path.join(abs_dic_path, f"{dic_name}.aff")
    print(f"Dictionary file exists: {os.path.isfile(dic_file)}")
    print(f"Affix file exists: {os.path.isfile(aff_file)}")
    
    # 절대 경로 출력
    print(f"Using dictionary path: {abs_dic_path}")
    
    # hunspell.exe의 절대 경로를 사용합니다.
    hunspell_cmd = [r'C:\msys64\mingw64\bin\hunspell.exe', '-a', '-d', dic_name]
    print(f"Hunspell command: {' '.join(hunspell_cmd)}")  # hunspell 명령어 출력
    
    try:
        process = subprocess.Popen(hunspell_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=abs_dic_path)
        stdout, stderr = process.communicate(input=text.encode('utf-8'))
        
        corrected_text = parse_hunspell_output(stdout.decode('utf-8', errors='ignore'), text)
        
        return corrected_text, stderr.decode('utf-8', errors='ignore')
    except Exception as e:
        return "", str(e)

def parse_hunspell_output(hunspell_output, original_text):
    lines = hunspell_output.splitlines()
    original_words = original_text.split()
    corrected_words = []
    
    i = 0
    for line in lines:
        if line.startswith('*'):
            corrected_words.append(original_words[i])
            i += 1
        elif line.startswith('&') or line.startswith('?'):
            parts = line.split()
            word = parts[1]
            suggestions = parts[4:]
            if suggestions:
                corrected_words.append(suggestions[0])
            else:
                corrected_words.append(word)
            i += 1
        elif line.startswith('+') or line.startswith('-'):
            # Handle other lines
            pass
    
    corrected_text = ' '.join(corrected_words)
    return corrected_text

# 맞춤법 검사를 할 텍스트
text = """사랑하는 가 충분히 사랑받지 못해서 미안해 
시간 Falling in love Let s Roll
겨우내 가 죽어요 그 댄 여리고 
너무 착해서 싫단 말도 못 잊어 
내 맘 깊은 곳에 난 문제 
라면 답없지 You can look and
우리 집에만 있니 take a lookie
하늘은 손 닿을 필요 없이 아름다운 
영화였 어우리가 돼 I m
땀 toasting with celebrities at the same
에 젖어 나의 신발난 가진 
게꿈밖에 없었네 눈 뜨면 잊는 
거야 그 사람 왔었나요 아니 소식이라도 
너의 사진 보겠지 새로 사귄 친구 
함께 웃음띤 네 얼굴에 네 
오마카세 I don t look
아리따운 날 입고 따 따랏따라 Baby
 SSAK Okay okay
널위해 준비된 내 마음 baby
이야 없었겠냐마는 그때 난 왜 몰랐을까 
이뤄질 수 없는 거 알아이 
가는 대로 칠해 시들 때도 예쁘게 
웃어주니 너처럼 좋은 여자가 왜 
눌렀니 참 바보 같은 맘인 걸 누가 
과연 누가 hot uh yeah hot uh
또 난동펴 H GHR GGANG
펴 펴 펴 펴 펴 펴펴 
니네 팀 분위기 다 초쳐 
가자 새벽에 닿을 때 우리 만날 
래 예쁘게 빛나던 모든 추억들보다 
괴로워 언제나 let s drink and have
 never known It all gets tangled up
자유롭게 뛰고 싶어 다른 사람 곁에 
안 좋은 결정했대 난 돈은 
쉽게 발을 빼 분명 네 꿈 
같은 순간이 바로 time to fly
넌 또 다른 나를 발견해 I
 will call ya I will be with
 that afterglow Show you what s up
우리 둘이 가을 Follow me"""
dic_path = r"C:\hunspell_dic"  # ko.dic과 ko.aff 파일이 있는 경로
dic_name = "ko"  # 사전 파일 이름 (확장자 없이)

# 맞춤법 검사 결과
stdout, stderr = check_spelling(text, dic_path, dic_name)

print("STDOUT:")
print(stdout)
print("STDERR:")
print(stderr)
