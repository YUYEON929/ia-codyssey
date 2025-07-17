import math # 원주율(pi)을 정확하게 사용하기 위해 math 모듈을 가져옵니다.

# --- 전역 변수 및 상수 정의 ---

# 1. 계산 결과를 저장할 전역 변수 (딕셔너리 형태)
calculation_result = {
    'material': '',
    'diameter': 0,
    'thickness': 0,
    'area': 0.0,
    'weight': 0.0
}

# 2. 프로그램에서 사용할 상수 정의
MATERIALS = {
    '유리': 2.4,
    '알루미늄': 2.7,
    '탄소강': 7.85
}
MARS_GRAVITY_RATIO = 0.38 # 화성 중력 / 지구 중력

# --- 함수 정의 ---

def sphere_area(diameter, material='유리', thickness=1):
    """
    반구의 겉넓이와 화성 기준 무게를 계산하는 함수
    
    Args:
        diameter (float): 돔의 지름 (단위: m)
        material (str, optional): 재질. 기본값 '유리'.
        thickness (int, optional): 두께 (단위: cm). 기본값 1.

    Returns:
        tuple: (계산된 겉넓이, 화성 기준 무게) 또는 오류 시 (None, None)
    """
    # --- 1. 단위 변환 및 기본 계산 ---
    # 지름(m)을 반지름(cm)으로 변환
    radius_cm = (diameter * 100) / 2
    
    # --- 2. 겉넓이 계산 ---
    # 반구의 겉넓이 공식: 2 * pi * r^2
    area = 2 * math.pi * (radius_cm ** 2)
    
    # --- 3. 무게 계산 ---
    # 두께(cm)를 이용해 부피(cm^3) 계산
    volume = area * thickness
    
    # 재질에 따른 밀도 선택 (g/cm^3)
    # .get()을 사용하면, 없는 키를 요청할 때 오류 대신 None을 반환해 안전합니다.
    density = MATERIALS.get(material)
    
    if density is None:
        print(f"오류: 알 수 없는 재질 '{material}'입니다. 계산을 중단합니다.")
        return None, None # 오류 발생 시 None 반환
    
    # 지구 기준 무게 계산 (g)
    earth_weight_g = volume * density
    
    # 화성 기준 무게 계산 (g)
    mars_weight_g = earth_weight_g * MARS_GRAVITY_RATIO
    
    # 화성 기준 무게를 kg으로 변환
    mars_weight_kg = mars_weight_g / 1000
    
    # 계산된 최종 값을 반환
    return area, mars_weight_kg


# --- 메인 실행 부분 ---

# 1. 사용자로부터 입력 받기
print("돔 설계를 시작합니다.")
# 지름은 필수 입력이므로, 숫자가 입력될 때까지 반복해서 물어볼 수 있습니다. (간단하게는 try-except 사용)
try:
    user_diameter = float(input("돔의 지름(m)을 입력하세요: "))
except ValueError:
    print("잘못된 입력입니다. 지름은 숫자여야 합니다. 프로그램을 종료합니다.")
    exit()

user_material = input("재질을 입력하세요 (유리, 알루미늄, 탄소강) [기본값: 유리]: ")
user_thickness_str = input("두께(cm)를 입력하세요 [기본값: 1cm]: ")


# 2. 입력값 처리 및 함수 호출
# 사용자가 재질을 입력하지 않았으면 기본값 '유리' 사용
if not user_material:
    user_material = '유리'

# 사용자가 두께를 입력했는지 확인하고 숫자로 변환
if user_thickness_str:
    try:
        user_thickness = float(user_thickness_str)
    except ValueError:
        print("잘못된 두께 값입니다. 기본값 1cm를 사용합니다.")
        user_thickness = 1.0
else:
    # 입력하지 않았으면 기본값 1 사용
    user_thickness = 1.0

# 설계한 함수를 호출하여 결과 받기
calculated_area, calculated_weight = sphere_area(
    diameter=user_diameter, 
    material=user_material, 
    thickness=user_thickness
)


# 3. 결과 처리 및 출력
# 함수가 정상적으로 값을 반환했을 때만 (None이 아닐 때) 결과를 처리
if calculated_area is not None and calculated_weight is not None:
    # 전역 변수에 계산 결과 저장
    calculation_result['material'] = user_material
    calculation_result['diameter'] = user_diameter
    calculation_result['thickness'] = user_thickness
    calculation_result['area'] = calculated_area
    calculation_result['weight'] = calculated_weight
    
    # 출력 형식에 맞춰 소수점 세 자리까지 포매팅하여 출력
    print("\n--- 계산 결과 ---")
    print(
        f"재질 ==> {calculation_result['material']}, "
        f"지름 ==> {calculation_result['diameter']:.3f} m, "
        f"두께 ==> {calculation_result['thickness']} cm, "
        f"면적 ==> {calculation_result['area']:.3f} cm², "
        f"무게 ==> {calculation_result['weight']:.3f} kg"
    )