import math # 원주율(pi)을 정확하게 사용하기 위해 math 모듈을 가져옵니다.

# --- 1. 프로그램에서 사용할 상수와 전역 변수 정의 ---

# 재질별 밀도(무게) 정보를 딕셔너리로 미리 정의합니다.
MATERIALS = {
    '유리': 2.4,
    '알루미늄': 2.7,
    '탄소강': 7.85
}
# 화성 중력 비율을 상수로 정의합니다.
MARS_GRAVITY_RATIO = 0.38

# 최종 계산 결과를 저장할 전역 변수 딕셔너리를 초기화합니다.
calculation_result = {
    'material': '',
    'diameter': 0.0,
    'thickness': 0.0,
    'area': 0.0,
    'weight': 0.0
}

# --- 2. 핵심 기능을 수행할 함수 정의 ---

def sphere_area(diameter, material='유리', thickness=1.0):
    """
    반구의 겉넓이와 화성 기준 무게를 계산합니다.

    Args:
        diameter (float): 돔의 지름 (단위: m)
        material (str, optional): 재질 이름. 기본값 '유리'.
        thickness (float, optional): 두께 (단위: cm). 기본값 1.0.

    Returns:
        tuple: (겉넓이(cm²), 무게(kg)) 쌍을 반환합니다.
               계산이 불가능할 경우 (None, None)을 반환합니다.
    """
    # 1단계: 단위 변환 (m -> cm) 및 반지름 계산
    radius_cm = (diameter * 100) / 2
    
    # 2단계: 반구의 겉넓이 계산 (2 * pi * r^2)
    area = 2 * math.pi * (radius_cm ** 2)
    
    # 3단계: 부피 계산 (겉넓이 * 두께)
    volume = area * thickness
    
    # 4단계: 재질에 따른 밀도(g/cm^3) 가져오기
    density = MATERIALS.get(material)
    
    # 5단계: 올바른 재질인지 확인
    if density is None:
        print(f"오류: 알 수 없는 재질 '{material}'입니다. 목록에 있는 재질을 입력해주세요.")
        return None, None # 계산 불가 시 None 반환
    
    # 6단계: 무게 계산 (g -> kg) 및 화성 중력 적용
    earth_weight_g = volume * density
    mars_weight_g = earth_weight_g * MARS_GRAVITY_RATIO
    mars_weight_kg = mars_weight_g / 1000
    
    return area, mars_weight_kg


# --- 3. 프로그램의 메인 실행 부분 ---

# 사용자로부터 각 값을 문자열(str)로 입력받습니다.
print("--- 돔 설계 프로그램 ---")
user_diameter_str = input("돔의 지름(m)을 입력하세요 [기본값: 10]: ")
user_material_str = input("재질을 입력하세요 (유리, 알루미늄, 탄소강) [기본값: 유리]: ")
user_thickness_str = input("두께(cm)를 입력하세요 [기본값: 1]: ")

# --- 4. 입력값 처리 및 기본값 설정 ---

# 지름 처리: 입력값이 있으면 숫자로 변환, 없거나 잘못되면 기본값 10.0 사용
if user_diameter_str:
    try:
        final_diameter = float(user_diameter_str)
    except ValueError:
        print("경고: 잘못된 지름 값입니다. 기본값 10m를 사용합니다.")
        final_diameter = 10.0
else:
    final_diameter = 10.0

# 재질 처리: 입력값이 없으면 기본값 '유리' 사용
if not user_material_str:
    final_material = '유리'
else:
    final_material = user_material_str

# 두께 처리: 입력값이 있으면 숫자로 변환, 없거나 잘못되면 기본값 1.0 사용
if user_thickness_str:
    try:
        final_thickness = float(user_thickness_str)
    except ValueError:
        print("경고: 잘못된 두께 값입니다. 기본값 1cm를 사용합니다.")
        final_thickness = 1.0
else:
    final_thickness = 1.0

# --- 5. 함수 호출 및 결과 저장 ---

# 처리된 최종 값들로 함수를 호출합니다.
calculated_area, calculated_weight = sphere_area(
    diameter=final_diameter, 
    material=final_material, 
    thickness=final_thickness
)

# --- 6. 최종 결과 출력 ---

# 함수가 정상적으로 계산을 마쳤을 경우에만 결과를 출력합니다.
if calculated_area is not None and calculated_weight is not None:
    # 전역 변수 딕셔너리에 최종 결과들을 저장합니다.
    calculation_result['material'] = final_material
    calculation_result['diameter'] = final_diameter
    calculation_result['thickness'] = final_thickness
    calculation_result['area'] = calculated_area
    calculation_result['weight'] = calculated_weight
    
    # f-string을 사용하여 형식에 맞춰 출력합니다. (소수점 3자리까지)
    print("\n--- 최종 계산 결과 ---")
    print(
        f"재질 ==> {calculation_result['material']}, "
        f"지름 ==> {calculation_result['diameter']:.3f} m, "
        f"두께 ==> {calculation_result['thickness']:.3f} cm, "
        f"면적 ==> {calculation_result['area']:.3f} cm², "
        f"무게 ==> {calculation_result['weight']:.3f} kg"
    )