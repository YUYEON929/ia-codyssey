# engineering_calculator.py
import sys
import math
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout,
                             QPushButton, QLineEdit)
from PyQt6.QtCore import Qt


class Calculator:
    def __init__(self):
        self.current_expression = ""
        self.operand1 = None
        self.operator = None
        self.waiting_for_operand2 = False
        self.memory = 0

    def clear(self):
        self.current_expression = ""
        self.operand1 = None
        self.operator = None
        self.waiting_for_operand2 = False
        return "0"

    def calculate(self):
        try:
            result = eval(self.current_expression)
            self.current_expression = str(result)
            return str(result)
        except Exception:
            return "Error"

    def handle_digit(self, digit):
        if self.waiting_for_operand2:
            self.current_expression = digit
            self.waiting_for_operand2 = False
        else:
            self.current_expression += digit
        return self.current_expression

    def handle_operator(self, op):
        if self.current_expression and not self.waiting_for_operand2:
            self.current_expression += op
            self.waiting_for_operand2 = False # 연산자 입력 후에도 숫자를 바로 이어서 입력할 수 있도록
        return self.current_expression

    def handle_equals(self):
        return self.calculate()

    def handle_ac(self):
        return self.clear()

    def handle_plus_minus(self):
        if self.current_expression and self.current_expression != "Error":
            if self.current_expression.startswith('-'):
                self.current_expression = self.current_expression[1:]
            else:
                self.current_expression = '-' + self.current_expression
        return self.current_expression

    def handle_percent(self):
        try:
            if self.current_expression and self.current_expression != "Error":
                value = float(self.current_expression) / 100
                self.current_expression = str(value)
                return self.current_expression
            return self.current_expression
        except ValueError:
            return "Error"

    # Memory functions
    def mc(self): # Memory Clear
        self.memory = 0
        return self.current_expression if self.current_expression else "0"

    def m_plus(self): # Memory Plus
        try:
            if self.current_expression:
                self.memory += float(eval(self.current_expression))
            return self.current_expression if self.current_expression else "0"
        except Exception:
            return "Error"

    def m_minus(self): # Memory Minus
        try:
            if self.current_expression:
                self.memory -= float(eval(self.current_expression))
            return self.current_expression if self.current_expression else "0"
        except Exception:
            return "Error"

    def mr(self): # Memory Recall
        self.current_expression = str(self.memory)
        return self.current_expression


class EngineeringCalculator(Calculator):
    def __init__(self):
        super().__init__()
        self.angle_unit = "Deg"  # "Deg" or "Rad"

    # 삼각함수 및 역삼각함수
    def _get_angle_value(self, value):
        if self.angle_unit == "Deg":
            return math.radians(value)
        return value

    def calculate_sin(self):
        try:
            value = float(eval(self.current_expression))
            result = math.sin(self._get_angle_value(value))
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def calculate_cos(self):
        try:
            value = float(eval(self.current_expression))
            result = math.cos(self._get_angle_value(value))
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def calculate_tan(self):
        try:
            value = float(eval(self.current_expression))
            result = math.tan(self._get_angle_value(value))
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def calculate_sinh(self):
        try:
            value = float(eval(self.current_expression))
            result = math.sinh(value)
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def calculate_cosh(self):
        try:
            value = float(eval(self.current_expression))
            result = math.cosh(value)
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def calculate_tanh(self):
        try:
            value = float(eval(self.current_expression))
            result = math.tanh(value)
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # 거듭제곱 및 제곱근
    def calculate_square(self): # x²
        try:
            value = float(eval(self.current_expression))
            result = value ** 2
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def calculate_cube(self): # x³
        try:
            value = float(eval(self.current_expression))
            result = value ** 3
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def calculate_power_y(self): # xʸ
        # 이 기능은 연산자처럼 동작하여 다음 숫자를 기다려야 합니다.
        # 현재 구현에서는 단순 eval로 처리하므로, 사용자가 직접 'x**y' 형태로 입력해야 합니다.
        # 복잡한 파싱 로직 없이 eval을 사용하기 위함입니다.
        self.current_expression += "**"
        self.waiting_for_operand2 = True
        return self.current_expression

    def calculate_exp(self): # eˣ
        try:
            value = float(eval(self.current_expression))
            result = math.exp(value)
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def calculate_ten_power(self): # 10ˣ
        try:
            value = float(eval(self.current_expression))
            result = 10 ** value
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def calculate_inverse(self): # 1/x
        try:
            value = float(eval(self.current_expression))
            if value == 0:
                return "Error"
            result = 1 / value
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def calculate_sqrt(self): # ²√x
        try:
            value = float(eval(self.current_expression))
            if value < 0:
                return "Error"
            result = math.sqrt(value)
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def calculate_cbrt(self): # ³√x
        try:
            value = float(eval(self.current_expression))
            result = value ** (1/3)
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def calculate_y_root(self): # ʸ√x
        # xʸ와 마찬가지로 'x**(1/y)' 형태로 입력해야 합니다.
        self.current_expression += "**(1/"
        self.waiting_for_operand2 = True
        return self.current_expression


    # 로그 함수
    def calculate_ln(self):
        try:
            value = float(eval(self.current_expression))
            if value <= 0:
                return "Error"
            result = math.log(value)
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def calculate_log10(self):
        try:
            value = float(eval(self.current_expression))
            if value <= 0:
                return "Error"
            result = math.log10(value)
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    # 기타 함수
    def calculate_factorial(self): # x!
        try:
            value = int(eval(self.current_expression))
            if value < 0:
                return "Error"
            result = math.factorial(value)
            self.current_expression = str(result)
            return self.current_expression
        except Exception:
            return "Error"

    def get_e(self): # e
        self.current_expression = str(math.e)
        return self.current_expression

    def handle_ee(self): # EE (지수 표기법)
        self.current_expression += "E"
        return self.current_expression

    def get_pi(self): # π
        self.current_expression = str(math.pi)
        return self.current_expression

    def get_rand(self): # Rand
        self.current_expression = str(math.random())
        return self.current_expression

    def toggle_angle_unit(self): # Deg/Rad
        if self.angle_unit == "Deg":
            self.angle_unit = "Rad"
        else:
            self.angle_unit = "Deg"
        return self.current_expression if self.current_expression else "0"


class EngineeringCalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator = EngineeringCalculator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Engineering Calculator")
        self.resize(600, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- 디스플레이 ---
        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 24px; padding: 10px;")
        layout.addWidget(self.display)

        # --- 버튼 레이아웃 ---
        grid = QGridLayout()
        layout.addLayout(grid)

        # 아이폰 공학용 계산기 버튼 배치
        buttons = [
            # 1행
            ("(", 0, 0), (")", 0, 1), ("mc", 0, 2), ("m+", 0, 3), ("m-", 0, 4), ("mr", 0, 5), ("AC", 0, 6), ("+/-", 0, 7), ("%", 0, 8), ("÷", 0, 9),
            # 2행
            ("2ⁿᵈ", 1, 0), ("x²", 1, 1), ("x³", 1, 2), ("xʸ", 1, 3), ("eˣ", 1, 4), ("10ˣ", 1, 5), ("7", 1, 6), ("8", 1, 7), ("9", 1, 8), ("×", 1, 9),
            # 3행
            ("1/x", 2, 0), ("²√x", 2, 1), ("³√x", 2, 2), ("ʸ√x", 2, 3), ("ln", 2, 4), ("log₁₀", 2, 5), ("4", 2, 6), ("5", 2, 7), ("6", 2, 8), ("-", 2, 9),
            # 4행
            ("x!", 3, 0), ("sin", 3, 1), ("cos", 3, 2), ("tan", 3, 3), ("e", 3, 4), ("EE", 3, 5), ("1", 3, 6), ("2", 3, 7), ("3", 3, 8), ("+", 3, 9),
            # 5행
            ("Deg", 4, 0), ("sinh", 4, 1), ("cosh", 4, 2), ("tanh", 4, 3), ("π", 4, 4), ("Rand", 4, 5), ("0", 4, 6, 1, 2), (".", 4, 8), ("=", 4, 9),
        ]

        # 버튼 생성 및 배치
        for text, row, col, *span in buttons:
            button = QPushButton(text)
            button.setFixedHeight(60)
            button.setStyleSheet("font-size: 16px;")
            if span:
                grid.addWidget(button, row, col, span[0], span[1])
            else:
                grid.addWidget(button, row, col)

            button.clicked.connect(lambda _, t=text: self.on_button_click(t))

    def on_button_click(self, text):
        """버튼을 누르면 디스플레이에 표시하고 계산"""
        result = ""
        if text.isdigit() or text == ".":
            result = self.calculator.handle_digit(text)
        elif text in ("+", "-", "×", "÷"):
            # eval 함수를 사용하기 위해 '×'를 '*'로, '÷'를 '/'로 변환
            op = text.replace("×", "*").replace("÷", "/")
            result = self.calculator.handle_operator(op)
        elif text == "=":
            result = self.calculator.handle_equals()
        elif text == "AC":
            result = self.calculator.handle_ac()
        elif text == "+/-":
            result = self.calculator.handle_plus_minus()
        elif text == "%":
            result = self.calculator.handle_percent()
        elif text == "(":
            self.calculator.current_expression += "("
            result = self.calculator.current_expression
        elif text == ")":
            self.calculator.current_expression += ")"
            result = self.calculator.current_expression
        # 메모리 기능
        elif text == "mc":
            result = self.calculator.mc()
        elif text == "m+":
            result = self.calculator.m_plus()
        elif text == "m-":
            result = self.calculator.m_minus()
        elif text == "mr":
            result = self.calculator.mr()
        # 공학용 계산기 기능
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
        elif text == "Deg": # Deg/Rad 토글
            self.calculator.toggle_angle_unit()
            # 버튼 텍스트를 업데이트하여 현재 단위를 표시할 수도 있습니다.
            # 하지만 여기서는 단순히 기능을 토글하고 디스플레이는 유지합니다.
            result = self.calculator.current_expression if self.calculator.current_expression else "0"
            sender_button = self.sender()
            if sender_button:
                sender_button.setText(self.calculator.angle_unit)
        elif text == "2ⁿᵈ":
            # 2ⁿᵈ 기능은 보통 다른 버튼들의 기능을 변경하는데 사용됩니다.
            # 이 예제에서는 2ⁿᵈ 관련 기능을 구현하지 않았으므로, 아무 동작도 하지 않습니다.
            pass


        self.display.setText(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EngineeringCalculatorUI()
    window.show()
    sys.exit(app.exec())