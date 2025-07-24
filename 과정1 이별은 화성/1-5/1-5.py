import numpy as np

# CSV 파일을 numpy로 읽기
arr1 = np.loadtxt('mars_base_main_parts-001.csv', delimiter=',', skiprows=1)
arr2 = np.loadtxt('mars_base_main_parts-002.csv', delimiter=',', skiprows=1)
arr3 = np.loadtxt('mars_base_main_parts-003.csv', delimiter=',', skiprows=1)

# 배열 합치기
parts = np.vstack((arr1, arr2, arr3))

# 각 항목(행)의 평균값 구하기
row_means = np.mean(parts, axis=1)

# 평균값이 50보다 작은 항목 선택
filtered_parts = parts[row_means < 50]

# 선택된 항목을 CSV로 저장
np.savetxt('parts_to_work_on.csv', filtered_parts, delimiter=',')

# 결과 출력 (선택)
print(f"총 항목 수: {parts.shape[0]}")
print(f"평균값이 50보다 작은 항목 수: {filtered_parts.shape[0]}")
