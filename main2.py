print ('Hello Mars')

# 파일 열고 출력하기
with open("mission_computer_main.log" , "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    print(line.strip())
