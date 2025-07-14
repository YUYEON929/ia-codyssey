#mission_computer_main.log 파일을 읽어들여서 출력한다. 콤마를 기준으로 날짜 및 시간과 로그 내용을 분류해서 Python의 리스트(List) 객체로 전환한다.
#(여기서 말하는 리스트는 배열이 아니라 파이썬에서 제공하는 리스트 타입의 객체를 의미한다.)
#전환된 리스트 객체를 화면에 출력한다.
#리스트 객체를 시간의 역순으로 정렬(sort)한다.
#리스트 객체를 사전(Dict) 객체로 전환한다.
#사전 객체로 전환된 내용을 mission_computer_main.json 파일로 저장하는데 파일 포멧은 JSON(JavaScript Ontation)으로 저장한다.


import json

log_list = []

with open('mission_computer_main.log','r', encoding='utf-8') as file:
    for line in file:
        if ',' in line:
            parts = line.strip().split(',')
            log_list.append(parts)
            
log_list.sort(key=lambda x:x[0],reverse=True)

print("===로그 리스트===")
for item in log_list:
   print(item) 
print("\n" + "="*50 + "\n")

log_dict = {}

for item in log_list:
        key = item[0]
        value = item[1]+item[2]
        log_dict[key] = value

print("===로그 딕셔너리===")
for k, v in log_dict.items():
#    print(f'k: {k}, v: {v}')
    print(k)
    print(v)
print("\n" + "="*50 + "\n")


with open('mission_computer_main.json','w',encoding='utf-8') as json_file:
    json.dump(log_dict, json_file, ensure_ascii=False, indent=4)




