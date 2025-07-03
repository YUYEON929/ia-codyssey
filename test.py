dic = {'name': 'pey', 'phone': '010-9999-1234', 'birth': '1118'}
dic[3] = 3
print(dic)

# dic.keys()는 모든 key를 순서대로 가져옵니다.
# list()로 감싸서 우리가 다루기 쉬운 리스트 형태로 바꿔줍니다.
all_keys = list(dic.keys()) 

print(f"{all_keys}")