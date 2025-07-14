#Mars_Base_Inventory_List.csv 의 내용을 읽어 들어서 출력한다.
#Mars_Base_Inventory_List.csv 내용을 읽어서 Python의 리스트(List) 객체로 변환한다.
#배열 내용을 적제 화물 목록을 인화성이 높은 순으로 정렬한다.
#인화성 지수가 0.7 이상되는 목록을 뽑아서 별도로 출력한다.
#인화성 지수가 0.7 이상되는 목록을 CSV 포멧(Mars_Base_Inventory_danger.csv)으로 저장한다.

#인화성 순서로 정렬된 배열의 내용을 이진 파일형태로 저장한다. 파일이름은 Mars_Base_Inventory_List.bin
#저장된 Mars_Base_Inventory_List.bin 의 내용을 다시 읽어 들여서 화면에 내용을 출력한다.
#텍스트 파일과 이진 파일 형태의 차이점을 설명하고 장단점을 함께 설명할 수 있게 준비한다.

import csv

log_list=[]
header = []

with open('Mars_Base_Inventory_List.csv','r',encoding='utf-8') as log_file:
    print('-----출력-----')
    
    header_line = log_file.readline()
    header = header_line.strip().split(',')
    print(header_line.strip())
    
    for line in log_file:
        if ','in line:
            parts = line.strip().split(',')
            parts[4] = float(parts[4])
            log_list.append(parts)
            print(line.strip())
print("\n" + "="*50 + "\n")

log_list.sort(key=lambda x:x[4],reverse=True)

print('-----인화성이 높은 순으로 정렬-----')
for item in log_list:
    print(item)
print("\n" + "="*50 + "\n")

danger_list = [item for item in log_list if item[4] >= 0.7] 
print('-----인화성 지수 0.7 이상 목록-----')
for item in danger_list:
    print(item)
print("\n" + "="*50 + "\n")

with open('Mars_Base_Inventory_danger.csv','w',encoding='utf-8',newline='') as danger_file:
    csv_writer = csv.writer(danger_file)
    csv_writer.writerow(header)
    csv_writer.writerows(danger_list)

log_list.sort(key=lambda x:x[4])

with open('Mars_Base_Inventory_List.bin','wb') as bin_file:
    import pickle
    pickle.dump(log_list,bin_file)

with open('Mars_Base_Inventory_List.bin','rb') as bin_file:
    import pickle
    loaded_list = pickle.load(bin_file)

print('--- 이진 파일에서 읽어온 데이터 ---')
print(header)
for item in loaded_list:
    print(item)