import numpy as np

def load_csv_file(file_name):
    data = np.genfromtxt(
        fname=file_name,
        delimiter=',',
        dtype=None,
        encoding='utf-8',
        skip_header=1
    )
    return data

def merge_files():
    arr1 = load_csv_file('mars_base_main_parts-001.csv')
    arr2 = load_csv_file('mars_base_main_parts-002.csv')
    arr3 = load_csv_file('mars_base_main_parts-003.csv')
    return np.concatenate((arr1, arr2, arr3), axis=0)

def calculate_average_strengths(parts):
    result = {}
    for row in parts:
        part_name = row[0]
        strength = float(row[1])
        if part_name not in result:
            result[part_name] = []
        result[part_name].append(strength)

    avg_result = []
    for part_name, strengths in result.items():
        avg = sum(strengths) / len(strengths)
        if avg < 50:
            avg_result.append((part_name, avg))
    return avg_result

def save_filtered_to_csv(data, file_name):
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('part,strength\n')
            for part_name, avg_strength in data:
                f.write(f'{part_name},{avg_strength:.2f}\n')
        print('파일이 성공적으로 저장되었습니다:', file_name)
    except IOError:
        print('파일 저장 중 오류가 발생했습니다:', file_name)

def main():
    parts = merge_files()
    filtered_averages = calculate_average_strengths(parts)
    save_filtered_to_csv(filtered_averages, 'parts_to_work_on.csv')

if __name__ == '__main__':
    main()
