# NumPy 라이브러리를 사용하기 위해 'np'라는 별명으로 불러옵니다.
import numpy as np

# --- 1단계: 3개의 CSV 파일을 각각 NumPy 배열로 읽어오기 ---

# 파일 이름들을 리스트로 관리합니다.
file_names = [
    'mars_base_main_parts-001.csv',
    'mars_base_main_parts-002.csv',
    'mars_base_main_parts-003.csv'
]

try:
    # 각 파일을 별도의 변수로 읽어옵니다.
    arr1 = np.genfromtxt(file_names[0], delimiter=',', dtype=None, encoding='utf-8', names=True)
    arr2 = np.genfromtxt(file_names[1], delimiter=',', dtype=None, encoding='utf-8', names=True)
    arr3 = np.genfromtxt(file_names[2], delimiter=',', dtype=None, encoding='utf-8', names=True)

except FileNotFoundError as e:
    print(f"오류: 파일을 찾을 수 없습니다. 파일 이름을 확인해주세요: {e}")
    exit()
except Exception as e:
    print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
    exit()


# --- 2단계: 3개의 배열을 하나로 합치기 ---

# np.concatenate() 함수를 사용해 세 배열을 하나로 합칩니다.
parts = np.concatenate((arr1, arr2, arr3))

print("--- 합쳐진 전체 부품(parts) 배열 ---")
print(parts)


# --- 3단계: 각 항목의 평균값 구하기 ---
# 'strength' 열만 사용한다고 가정합니다.
averages = parts['strength']

print("\n--- 각 부품의 평균(strength) 값 ---")
print(averages)


# --- 4단계: 평균값이 50보다 작은 값만 뽑기 ---
parts_to_work_on = parts[averages < 50]

print("\n--- 평균(strength)값이 50 미만인 부품 목록 ---")
print(parts_to_work_on)


# --- 5단계: 결과를 새로운 CSV 파일로 저장하기 ---
output_file_name = 'parts_to_work_on.csv'

header = 'parts,strength'

try:
    np.savetxt(output_file_name, parts_to_work_on, delimiter=',', fmt='%s,%.2f', header=header, comments='')
    print(f"\n'{output_file_name}' 파일이 성공적으로 저장되었습니다.")
except Exception as e:
    print(f"\n파일 저장 중 오류가 발생했습니다: {e}")
