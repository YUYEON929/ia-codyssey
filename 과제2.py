import json

# 1️⃣ 로그 파일 열기
file_name = "mission_computer_main.log"

with open(file_name, "r", encoding="utf-8") as file:
    lines = file.readlines()

# 2️⃣ 콤마로 나눠서 리스트로 만들기
log_list = []  # 빈 리스트 만들기

for line in lines:
    parts = line.strip().split(",")  # 콤마로 자르고 양쪽 공백 제거
    timestamp = parts[0].strip()
    event = parts[1].strip()
    message = parts[2].strip()
    # [날짜 및 시간, 로그 내용] 구조로 리스트에 추가
    log_list.append([timestamp, f"{event}, {message}"])

# 3️⃣ 리스트 출력하기
print("=== 로그 리스트 ===")
for item in log_list:
    print(item)

# 4️⃣ 시간 역순으로 정렬하기
# 시간순으로 정렬 후 역순으로 뒤집기 (문자열 비교 가능)
log_list.sort(reverse=True, key=lambda x: x[0])

print("\n=== 시간 역순으로 정렬된 리스트 ===")
for item in log_list:
    print(item)

# 5️⃣ 리스트를 사전(Dict)으로 바꾸기
# 키: timestamp, 값: 로그 내용
log_dict = {item[0]: item[1] for item in log_list}

# 6️⃣ 사전을 JSON 파일로 저장하기
json_file_name = "mission_computer_main.json"

with open(json_file_name, "w", encoding="utf-8") as json_file:
    json.dump(log_dict, json_file, ensure_ascii=False, indent=4)

print(f"\nJSON 파일로 저장 완료! → {json_file_name}")
