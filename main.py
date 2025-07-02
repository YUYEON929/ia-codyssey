print ('Hello Mars')

import os

# 사용자 이름
user_name = "apple"

# 바탕화면 안의 '코디세이' 폴더 경로 만들기
base_path = os.path.join("C:/Users", user_name, "OneDrive", "바탕 화면", "codyssey")

# 파일 이름
file_name = "mission_computer_main.log"

# 전체 경로
file_path = os.path.join(base_path, file_name)

# 파일 열고 출력하기
with open(file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    print(line.strip())
