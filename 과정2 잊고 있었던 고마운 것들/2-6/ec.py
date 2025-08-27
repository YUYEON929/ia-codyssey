# engineering_calculator.py

# 1. 필요한 모듈들을 가져옵니다.
import sys  # 시스템 관련 기능 (예: 프로그램 종료)을 사용하기 위해 sys 모듈을 가져옵니다.
import math # 수학 함수 (삼각함수, 로그, 제곱근 등)를 사용하기 위해 math 모듈을 가져옵니다.

# PyQt6 라이브러리에서 GUI (그래픽 사용자 인터페이스)를 구성하는 데 필요한 클래스들을 가져옵니다.
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout,
                             QPushButton, QLineEdit)
from PyQt6.QtCore import Qt # Qt 모듈에서 특정 상수 (예: 텍스트 정렬)를 사용하기 위해 Qt를 가져옵니다.


# 2. 기본 계산기 기능을 정의하는 Calculator 클래스입니다.
# 이 클래스는 사칙연산, 퍼센트, 부호 변경, 메모리 기능 등의 기본적인 계산 로직을 담당합니다.
class Calculator:
    def __init__(self):
        # 계산기의 현재 상태를 초기화합니다.
        self.current_expression = ""  # 현재 화면에 표시되거나 계산될 수식 또는 숫자를 저장합니다.
        self.operand1 = None          # 첫 번째 피연산자를 저장합니다. (현재 구현에서는 eval을 주로 사용해 직접 활용되지는 않습니다.)
        self.operator = None          # 현재 선택된 연산자를 저장합니다. (현재 구현에서는 eval을 주로 사용해 직접 활용되지는 않습니다.)
        self.waiting_for_operand2 = False # 연산자 입력 후 두 번째 숫자를 기다리는 상태인지 나타냅니다. (현재 구현에서는 eval을 주로 사용해 직접 활용되지는 않습니다.)
        self.memory = 0               # 메모리 기능을 위한 값을 저장합니다.

    # 계산기 상태를 초기화하고 디스플레이를 "0"으로 만드는 메서드입니다.
    def clear(self):
        self.current_expression = ""
        self.operand1 = None
        self.operator = None
        self.waiting_for_operand2 = False
        return "0"  # 디스플레이에 "0"을 표시하도록 반환합니다.

    # 현재 current_expression에 있는 수식을 계산하는 메서드입니다.
    def calculate(self):
        try:
            # eval() 함수는 문자열로 된 파이썬 표현식을 실행하여 결과를 반환합니다.
            # 예: "1+2*3" -> 7
            result = eval(self.current_expression)
            self.current_expression = str(result) # 계산 결과를 문자열로 변환하여 저장합니다.
            return str(result) # 디스플레이에 표시하기 위해 결과를 문자열로 반환합니다.
        except Exception: # 계산 중 오류가 발생하면 (예: 잘못된 수식)
            return "Error"  # "Error" 문자열을 반환합니다.

    # 숫자 버튼이 눌렸을 때 호출되는 메서드입니다.
    def handle_digit(self, digit):
        if self.waiting_for_operand2: # 만약 이전에 연산자가 눌러져 다음 숫자를 기다리는 상태라면
            self.current_expression = digit # 새로운 숫자로 current_expression을 시작합니다.
            self.waiting_for_operand2 = False # 더 이상 다음 숫자를 기다리지 않습니다.
        else: # 그렇지 않다면 (이전 숫자에 이어서 입력하는 경우)
            self.current_expression += digit # 현재 수식에 숫자를 추가합니다.
        return self.current_expression # 업데이트된 수식을 반환하여 디스플레이에 표시합니다.

    # 연산자 버튼이 눌렸을 때 호출되는 메서드입니다.
    def handle_operator(self, op):
        # current_expression이 비어있지 않고, 다음 숫자를 기다리는 상태가 아니라면
        if self.current_expression and not self.waiting_for_operand2:
            self.current_expression += op # 현재 수식에 연산자를 추가합니다.
            self.waiting_for_operand2 = False # 연산자 입력 후에도 숫자를 바로 이어서 입력할 수 있도록 상태를 유지합니다.
        return self.current_expression # 업데이트된 수식을 반환합니다.

    # 등호 '=' 버튼이 눌렸을 때 호출되는 메서드입니다.
    def handle_equals(self):
        return self.calculate() # calculate 메서드를 호출하여 최종 결과를 반환합니다.

    # 'AC' (All Clear) 버튼이 눌렸을 때 호출되는 메서드입니다.
    def handle_ac(self):
        return self.clear() # clear 메서드를 호출하여 계산기를 초기화합니다.

    # '+/-' (부호 변경) 버튼이 눌렸을 때 호출되는 메서드입니다.
    def handle_plus_minus(self):
        # 현재 수식이 비어있지 않고 "Error"가 아니라면
        if self.current_expression and self.current_expression != "Error":
            if self.current_expression.startswith('-'): # 만약 현재 수식이 음수라면 ('-'로 시작)
                self.current_expression = self.current_expression[1:] # 맨 앞의 '-'를 제거하여 양수로 만듭니다.
            else: # 현재 수식이 양수라면
                self.current_expression = '-' + self.current_expression # 맨 앞에 '-'를 붙여 음수로 만듭니다.
        return self.current_expression # 업데이트된 수식을 반환합니다.

    # '%' (퍼센트) 버튼이 눌렸을 때 호출되는 메서드입니다.
    def handle_percent(self):
        try:
            # 현재 수식이 비어있지 않고 "Error"가 아니라면
            if self.current_expression and self.current_expression != "Error":
                value = float(self.current_expression) / 100 # 현재 값을 숫자로 변환하여 100으로 나눕니다.
                self.current_expression = str(value) # 결과를 문자열로 변환하여 저장합니다.
                return self.current_expression
            return self.current_expression # 조건에 맞지 않으면 현재 수식을 그대로 반환합니다.
        except ValueError: # 숫자로 변환할 수 없는 경우 (예: "abc%")
            return "Error" # "Error"를 반환합니다.

    # 메모리 관련 함수들입니다.
    def mc(self): # Memory Clear (메모리 지우기)
        self.memory = 0 # 메모리 값을 0으로 초기화합니다.
        # current_expression이 있으면 그 값을, 없으면 "0"을 반환합니다.
        return self.current_expression if self.current_expression else "0"

    def m_plus(self): # Memory Plus (메모리에 현재 값 더하기)
        try:
            if self.current_expression: # 현재 수식이 비어있지 않다면
                # 현재 수식을 계산한 후 그 결과를 float형으로 변환하여 메모리에 더합니다.
                self.memory += float(eval(self.current_expression))
            return self.current_expression if self.current_expression else "0"
        except Exception:
            return "Error"

    def m_minus(self): # Memory Minus (메모리에서 현재 값 빼기)
        try:
            if self.current_expression: # 현재 수식이 비어있지 않다면
                # 현재 수식을 계산한 후 그 결과를 float형으로 변환하여 메모리에서 뺍니다.
                self.memory -= float(eval(self.current_expression))
            return self.current_expression if self.current_expression else "0"
        except Exception:
            return "Error"

    def mr(self): # Memory Recall (메모리 값 불러오기)
        self.current_expression = str(self.memory) # 메모리에 저장된 값을 문자열로 변환하여 current_expression에 설정합니다.
        return self.current_expression # 메모리 값을 반환합니다.


# 3. 공학용 계산기 기능을 추가한 EngineeringCalculator 클래스입니다.
# Calculator 클래스를 상속받아(기존 기능을 재사용하면서) 공학 계산 기능을 확장합니다.
class EngineeringCalculator(Calculator):
    def __init__(self):
        super().__init__()               # 부모 클래스인 Calculator의 __init__ 메서드를 호출하여 초기화합니다.
        self.angle_unit = "Deg"  # 각도 단위를 "Deg" (도) 또는 "Rad" (라디안)으로 설정합니다. 초기값은 "Deg"입니다.

    # --- 삼각함수 및 역삼각함수 관련 메서드 ---
    # 현재 설정된 각도 단위("Deg" 또는 "Rad")에 따라 값을 math 모듈이 사용하는 라디안으로 변환합니다.
    def _get_angle_value(self, value):
        if self.angle_unit == "Deg":     # 각도 단위가 "Deg" (도)이면
            return math.radians(value)   # math.radians()를 사용하여 도를 라디안으로 변환합니다.
        return value                     # "Rad" (라디안)이면 값을 그대로 반환합니다.

    # sin 함수를 계산하는 메서드입니다.
    def calculate_sin(self):
        try:
            value = float(eval(self.current_expression)) # 현재 수식을 계산하여 숫자로 변환합니다.
            result = math.sin(self._get_angle_value(value)) # 각도 단위를 고려하여 sin 값을 계산합니다.
            self.current_expression = str(result) # 결과를 문자열로 저장합니다.
            return self.current_expression
        except Exception:
            return "Error"

    # cos 함수를 계산하는 메서드입니다.
    def calculate_cos(self):
        try:
            value = float(eval(self.current_expression))
            result = math.cos(self._get_angle_value(value)) # 각도 단위를 고려하여 cos 값을 계산합니다.
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # tan 함수를 계산하는 메서드입니다.
    def calculate_tan(self):
        try:
            value = float(eval(self.current_expression))
            result = math.tan(self._get_angle_value(value)) # 각도 단위를 고려하여 tan 값을 계산합니다.
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # sinh (쌍곡선 사인) 함수를 계산하는 메서드입니다.
    def calculate_sinh(self):
        try:
            value = float(eval(self.current_expression))
            result = math.sinh(value)
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # cosh (쌍곡선 코사인) 함수를 계산하는 메서드입니다.
    def calculate_cosh(self):
        try:
            value = float(eval(self.current_expression))
            result = math.cosh(value)
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # tanh (쌍곡선 탄젠트) 함수를 계산하는 메서드입니다.
    def calculate_tanh(self):
        try:
            value = float(eval(self.current_expression))
            result = math.tanh(value)
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # --- 거듭제곱 및 제곱근 관련 메서드 ---
    # x² (제곱)을 계산하는 메서드입니다.
    def calculate_square(self):
        try:
            value = float(eval(self.current_expression))
            result = value ** 2 # 값을 제곱합니다.
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # x³ (세제곱)을 계산하는 메서드입니다.
    def calculate_cube(self):
        try:
            value = float(eval(self.current_expression))
            result = value ** 3 # 값을 세제곱합니다.
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # xʸ (x의 y제곱) 기능을 처리하는 메서드입니다.
    # eval()을 사용하기 위해 수식에 '**'를 추가하고 다음 숫자 입력을 기다립니다.
    def calculate_power_y(self):
        self.current_expression += "**" # 파이썬에서 거듭제곱 연산자(**)를 수식에 추가합니다.
        self.waiting_for_operand2 = True # 다음 숫자가 지수(y)가 될 것임을 나타냅니다.
        return self.current_expression

    # eˣ (자연로그의 밑 e의 x제곱)을 계산하는 메서드입니다.
    def calculate_exp(self):
        try:
            value = float(eval(self.current_expression))
            result = math.exp(value) # math.exp() 함수로 계산합니다.
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # 10ˣ (10의 x제곱)을 계산하는 메서드입니다.
    def calculate_ten_power(self):
        try:
            value = float(eval(self.current_expression))
            result = 10 ** value # 10의 거듭제곱을 계산합니다.
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # 1/x (역수)를 계산하는 메서드입니다.
    def calculate_inverse(self):
        try:
            value = float(eval(self.current_expression))
            if value == 0: # 0으로 나누는 것은 오류이므로
                return "Error"
            result = 1 / value
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # ²√x (제곱근)을 계산하는 메서드입니다.
    def calculate_sqrt(self):
        try:
            value = float(eval(self.current_expression))
            if value < 0: # 음수의 제곱근은 허수이므로 오류 처리합니다.
                return "Error"
            result = math.sqrt(value) # math.sqrt() 함수로 계산합니다.
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # ³√x (세제곱근)을 계산하는 메서드입니다.
    def calculate_cbrt(self):
        try:
            value = float(eval(self.current_expression))
            result = value ** (1/3) # 값을 1/3 제곱하여 세제곱근을 구합니다.
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # ʸ√x (y제곱근) 기능을 처리하는 메서드입니다.
    # eval()을 사용하기 위해 수식에 '**(1/'를 추가하고 다음 숫자 입력을 기다립니다.
    def calculate_y_root(self):
        self.current_expression += "**(1/" # y제곱근은 x의 (1/y)제곱과 같습니다.
        self.waiting_for_operand2 = True # 다음 숫자가 y 값이 될 것임을 나타냅니다.
        return self.current_expression


    # --- 로그 함수 관련 메서드 ---
    # ln (자연로그)를 계산하는 메서드입니다.
    def calculate_ln(self):
        try:
            value = float(eval(self.current_expression))
            if value <= 0: # 0 이하의 값은 자연로그를 계산할 수 없습니다.
                return "Error"
            result = math.log(value) # math.log()는 기본적으로 자연로그를 계산합니다.
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # log₁₀ (상용로그, 밑이 10인 로그)를 계산하는 메서드입니다.
    def calculate_log10(self):
        try:
            value = float(eval(self.current_expression))
            if value <= 0: # 0 이하의 값은 상용로그를 계산할 수 없습니다.
                return "Error"
            result = math.log10(value) # math.log10() 함수로 계산합니다.
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # --- 기타 함수 관련 메서드 ---
    # x! (팩토리얼)을 계산하는 메서드입니다.
    def calculate_factorial(self):
        try:
            value = int(eval(self.current_expression)) # 값을 정수로 변환합니다.
            if value < 0: # 음수의 팩토리얼은 정의되지 않습니다.
                return "Error"
            result = math.factorial(value) # math.factorial() 함수로 계산합니다.
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # 상수 e (자연로그의 밑) 값을 가져오는 메서드입니다.
    def get_e(self):
        self.current_expression = str(math.e) # math.e 상수를 문자열로 current_expression에 설정합니다.
        return self.current_expression

    # EE (지수 표기법) 버튼을 처리하는 메서드입니다.
    # 예: 1.23E+05 와 같이 E를 추가합니다.
    def handle_ee(self):
        self.current_expression += "E" # 수식에 문자 'E'를 추가합니다.
        return self.current_expression

    # 상수 π (파이) 값을 가져오는 메서드입니다.
    def get_pi(self):
        self.current_expression = str(math.pi) # math.pi 상수를 문자열로 current_expression에 설정합니다.
        return self.current_expression

    # Rand (난수)를 생성하는 메서드입니다.
    def get_rand(self):
        # NOTE: math 모듈에는 random() 함수가 직접 없습니다.
        # 일반적으로 'random' 모듈의 'random.random()'을 사용해야 합니다.
        # 현재 코드로는 AttributeError가 발생할 수 있습니다.
        # 올바른 구현을 위해서는 'import random' 후 'random.random()'을 사용해야 합니다.
        self.current_expression = str(math.random())
        return self.current_expression

    # Deg/Rad (각도 단위)를 토글하는 메서드입니다.
    def toggle_angle_unit(self):
        if self.angle_unit == "Deg": # 현재 단위가 "Deg"이면
            self.angle_unit = "Rad"  # "Rad"로 변경합니다.
        else:                        # 현재 단위가 "Rad"이면
            self.angle_unit = "Deg"  # "Deg"로 변경합니다.
        # current_expression이 있으면 그 값을, 없으면 "0"을 반환합니다.
        return self.current_expression if self.current_expression else "0"


# 4. 공학용 계산기의 사용자 인터페이스 (UI)를 정의하는 EngineeringCalculatorUI 클래스입니다.
# 이 클래스는 PyQt6를 사용하여 계산기 창, 디스플레이, 버튼 등을 만들고, 사용자 상호작용을 처리합니다.
class EngineeringCalculatorUI(QWidget): # QWidget을 상속받아 새로운 위젯(창)을 만듭니다.
    def __init__(self):
        super().__init__()               # 부모 클래스인 QWidget의 __init__ 메서드를 호출합니다.
        self.calculator = EngineeringCalculator() # 공학 계산 로직을 처리할 EngineeringCalculator 객체를 생성합니다.
        self.init_ui()                   # 사용자 인터페이스를 초기화하는 메서드를 호출합니다.

    # 사용자 인터페이스를 설정하는 메서드입니다.
    def init_ui(self):
        self.setWindowTitle("Engineering Calculator") # 창의 제목을 설정합니다.
        self.resize(600, 400)          # 창의 초기 크기를 너비 600px, 높이 400px로 설정합니다.

        layout = QVBoxLayout()           # 전체 위젯을 세로로 배치하기 위한 QVBoxLayout을 생성합니다.
        self.setLayout(layout)           # 이 창의 주된 레이아웃으로 설정합니다.

        # --- 디스플레이 (계산 결과가 표시되는 부분) ---
        self.display = QLineEdit("0")    # 한 줄 텍스트를 표시하는 QLineEdit 위젯을 생성하고 초기값 "0"을 설정합니다.
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight) # 텍스트를 오른쪽으로 정렬합니다.
        self.display.setReadOnly(True)   # 사용자가 직접 텍스트를 편집할 수 없도록 읽기 전용으로 설정합니다.
        self.display.setStyleSheet("font-size: 24px; padding: 10px;") # CSS 스타일시트를 적용하여 글꼴 크기와 패딩을 설정합니다.
        layout.addWidget(self.display)   # 디스플레이 위젯을 메인 레이아웃에 추가합니다.

        # --- 버튼 레이아웃 ---
        grid = QGridLayout()             # 버튼들을 격자(Grid) 형태로 배치하기 위한 QGridLayout을 생성합니다.
        layout.addLayout(grid)           # 이 격자 레이아웃을 메인 레이아웃에 추가합니다.

        # 아이폰 공학용 계산기와 유사한 버튼 배치를 정의합니다.
        # 각 튜플은 (버튼 텍스트, 행 번호, 열 번호, [선택적: 행 스팬, 열 스팬])을 나타냅니다.
        buttons = [
            # 1행 버튼들
            ("(", 0, 0), (")", 0, 1), ("mc", 0, 2), ("m+", 0, 3), ("m-", 0, 4), ("mr", 0, 5), ("AC", 0, 6), ("+/-", 0, 7), ("%", 0, 8), ("÷", 0, 9),
            # 2행 버튼들
            ("2ⁿᵈ", 1, 0), ("x²", 1, 1), ("x³", 1, 2), ("xʸ", 1, 3), ("eˣ", 1, 4), ("10ˣ", 1, 5), ("7", 1, 6), ("8", 1, 7), ("9", 1, 8), ("×", 1, 9),
            # 3행 버튼들
            ("1/x", 2, 0), ("²√x", 2, 1), ("³√x", 2, 2), ("ʸ√x", 2, 3), ("ln", 2, 4), ("log₁₀", 2, 5), ("4", 2, 6), ("5", 2, 7), ("6", 2, 8), ("-", 2, 9),
            # 4행 버튼들
            ("x!", 3, 0), ("sin", 3, 1), ("cos", 3, 2), ("tan", 3, 3), ("e", 3, 4), ("EE", 3, 5), ("1", 3, 6), ("2", 3, 7), ("3", 3, 8), ("+", 3, 9),
            # 5행 버튼들
            ("Deg", 4, 0), ("sinh", 4, 1), ("cosh", 4, 2), ("tanh", 4, 3), ("π", 4, 4), ("Rand", 4, 5), ("0", 4, 6, 1, 2), (".", 4, 8), ("=", 4, 9),
        ]

        # 정의된 버튼 리스트를 순회하며 버튼을 생성하고 격자 레이아웃에 배치합니다.
        for text, row, col, *span in buttons:
            button = QPushButton(text)       # QPushButton을 생성하고 버튼 텍스트를 설정합니다.
            button.setFixedHeight(60)        # 버튼의 고정 높이를 설정합니다.
            button.setStyleSheet("font-size: 16px;") # 버튼의 글꼴 크기를 설정합니다.
            if span:                         # 만약 행/열 스팬 정보가 있다면 (예: '0' 버튼처럼 여러 칸 차지)
                grid.addWidget(button, row, col, span[0], span[1]) # 해당 스팬을 적용하여 배치합니다.
            else:                            # 스팬 정보가 없다면 (기본 1칸)
                grid.addWidget(button, row, col) # 기본 1칸으로 배치합니다.

            # 각 버튼이 클릭될 때 `on_button_click` 메서드가 호출되도록 연결합니다.
            # `lambda` 함수를 사용하여 현재 버튼의 텍스트(t=text)를 인자로 전달합니다.
            button.clicked.connect(lambda _, t=text: self.on_button_click(t))

    # 버튼이 클릭되었을 때 호출되는 메서드입니다.
    def on_button_click(self, text):
        """버튼을 누르면 디스플레이에 표시하고 계산 로직을 호출합니다."""
        result = ""
        if text.isdigit() or text == ".": # 눌린 버튼이 숫자이거나 소수점이라면
            result = self.calculator.handle_digit(text) # calculator 객체의 handle_digit 메서드를 호출합니다.
        elif text in ("+", "-", "×", "÷"): # 눌린 버튼이 사칙연산자라면
            # eval() 함수가 이해할 수 있도록 '×'를 '*'로, '÷'를 '/'로 변환합니다.
            op = text.replace("×", "*").replace("÷", "/")
            result = self.calculator.handle_operator(op) # calculator 객체의 handle_operator 메서드를 호출합니다.
        elif text == "=": # 등호 버튼이라면
            result = self.calculator.handle_equals() # calculator 객체의 handle_equals 메서드를 호출합니다.
        elif text == "AC": # 'AC' 버튼이라면
            result = self.calculator.handle_ac() # calculator 객체의 handle_ac 메서드를 호출합니다.
        elif text == "+/-": # 부호 변경 버튼이라면
            result = self.calculator.handle_plus_minus() # calculator 객체의 handle_plus_minus 메서드를 호출합니다.
        elif text == "%": # 퍼센트 버튼이라면
            result = self.calculator.handle_percent() # calculator 객체의 handle_percent 메서드를 호출합니다.
        elif text == "(": # 여는 괄호 버튼이라면
            self.calculator.current_expression += "("
            result = self.calculator.current_expression
        elif text == ")": # 닫는 괄호 버튼이라면
            self.calculator.current_expression += ")"
            result = self.calculator.current_expression
        # 메모리 기능 버튼들
        elif text == "mc":
            result = self.calculator.mc()
        elif text == "m+":
            result = self.calculator.m_plus()
        elif text == "m-":
            result = self.calculator.m_minus()
        elif text == "mr":
            result = self.calculator.mr()
        # 공학용 계산기 기능 버튼들
        elif text == "sin":
            result = self.calculator.calculate_sin()
        elif text == "cos":
            result = self.calculator.calculate_cos()
        elif text == "tan":
            result = self.calculator.calculate_tan()
        elif text == "sinh":
            result = self.calculator.calculate_sinh()
        elif text == "cosh":
            result = self.calculator.calculate_cosh()
        elif text == "tanh":
            result = self.calculator.calculate_tanh()
        elif text == "x²":
            result = self.calculator.calculate_square()
        elif text == "x³":
            result = self.calculator.calculate_cube()
        elif text == "xʸ":
            result = self.calculator.calculate_power_y()
        elif text == "eˣ":
            result = self.calculator.calculate_exp()
        elif text == "10ˣ":
            result = self.calculator.calculate_ten_power()
        elif text == "1/x":
            result = self.calculator.calculate_inverse()
        elif text == "²√x":
            result = self.calculator.calculate_sqrt()
        elif text == "³√x":
            result = self.calculator.calculate_cbrt()
        elif text == "ʸ√x":
            result = self.calculator.calculate_y_root()
        elif text == "ln":
            result = self.calculator.calculate_ln()
        elif text == "log₁₀":
            result = self.calculator.calculate_log10()
        elif text == "x!":
            result = self.calculator.calculate_factorial()
        elif text == "e":
            result = self.calculator.get_e()
        elif text == "EE":
            result = self.calculator.handle_ee()
        elif text == "π":
            result = self.calculator.get_pi()
        elif text == "Rand":
            result = self.calculator.get_rand()
        elif text == "Deg": # 'Deg/Rad' 토글 버튼이라면
            self.calculator.toggle_angle_unit() # 각도 단위를 토글합니다.
            sender_button = self.sender()       # 이벤트를 발생시킨 버튼 객체를 가져옵니다.
            if sender_button:
                sender_button.setText(self.calculator.angle_unit) # 버튼의 텍스트를 현재 각도 단위로 업데이트합니다.
            # current_expression이 있으면 그 값을, 없으면 "0"을 반환합니다.
            result = self.calculator.current_expression if self.calculator.current_expression else "0"
        elif text == "2ⁿᵈ":
            # "2ⁿᵈ" (세컨드) 기능은 다른 버튼들의 기능을 변경하는 데 사용되지만,
            # 이 예제에서는 해당 기능이 구현되어 있지 않으므로 아무 동작도 하지 않습니다.
            pass

        self.display.setText(result) # 계산 결과를 디스플레이 QLineEdit에 업데이트하여 화면에 표시합니다.


# 5. 스크립트가 직접 실행될 때만 다음 코드를 실행합니다.
# 이 부분이 PyQt6 애플리케이션을 시작하고 실행하는 역할입니다.
if __name__ == "__main__":
    app = QApplication(sys.argv) # QApplication 객체를 생성하여 PyQt6 애플리케이션을 초기화합니다.
                                 # sys.argv는 명령줄 인수를 애플리케이션에 전달합니다.
    window = EngineeringCalculatorUI() # EngineeringCalculatorUI 객체를 생성하여 계산기 창을 만듭니다.
    window.show()                # 계산기 창을 화면에 표시합니다.
    sys.exit(app.exec())         # PyQt6 이벤트 루프를 시작하고, 애플리케이션이 종료될 때까지 대기합니다.
                                 # 사용자가 창을 닫으면 이벤트 루프가 종료되고, 프로그램이 안전하게 종료됩니다.