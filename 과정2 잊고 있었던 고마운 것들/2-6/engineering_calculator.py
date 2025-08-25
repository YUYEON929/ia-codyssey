# engineering_calculator.py
import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout
)
from PyQt6.QtCore import Qt


# --- 기본 계산기 클래스 ---
class Calculator:
    def __init__(self):
        self.display_value = ""

    def clear(self):
        self.display_value = ""

    def append(self, value):
        self.display_value += str(value)

    def get_display(self):
        return self.display_value

    def calculate(self):
        try:
            result = eval(self.display_value)
            self.display_value = str(result)
        except Exception:
            self.display_value = "Error"


# --- 공학용 계산기 클래스 ---
class EngineeringCalculator(Calculator, QWidget):
    def __init__(self):
        Calculator.__init__(self)
        QWidget.__init__(self)
        self.setWindowTitle("Engineering Calculator")
        self.setFixedSize(600, 400)
        self.init_ui()

    # 📌 공학용 추가 기능 (30개 중 일부 구현)
    def func_sin(self):
        try:
            value = float(self.display_value)
            self.display_value = str(math.sin(math.radians(value)))
        except:
            self.display_value = "Error"

    def func_cos(self):
        try:
            value = float(self.display_value)
            self.display_value = str(math.cos(math.radians(value)))
        except:
            self.display_value = "Error"

    def func_tan(self):
        try:
            value = float(self.display_value)
            self.display_value = str(math.tan(math.radians(value)))
        except:
            self.display_value = "Error"

    def func_sinh(self):
        try:
            value = float(self.display_value)
            self.display_value = str(math.sinh(value))
        except:
            self.display_value = "Error"

    def func_cosh(self):
        try:
            value = float(self.display_value)
            self.display_value = str(math.cosh(value))
        except:
            self.display_value = "Error"

    def func_tanh(self):
        try:
            value = float(self.display_value)
            self.display_value = str(math.tanh(value))
        except:
            self.display_value = "Error"

    def func_pi(self):
        self.display_value = str(math.pi)

    def func_square(self):
        try:
            value = float(self.display_value)
            self.display_value = str(value ** 2)
        except:
            self.display_value = "Error"

    def func_cube(self):
        try:
            value = float(self.display_value)
            self.display_value = str(value ** 3)
        except:
            self.display_value = "Error"

    # --- UI 초기화 ---
    def init_ui(self):
        layout = QVBoxLayout()

        # 출력창
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 24px; padding: 10px;")
        layout.addWidget(self.display)

        # 버튼 배열
        buttons = [
            ["sin", "cos", "tan", "sinh", "cosh", "tanh"],
            ["π", "x²", "x³", "AC", "=", "+"],
            ["7", "8", "9", "-"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "÷"],
            ["0", ".", "%"]
        ]

        grid = QGridLayout()
        layout.addLayout(grid)

        row = 0
        for row_buttons in buttons:
            col = 0
            for btn_text in row_buttons:
                btn = QPushButton(btn_text)
                btn.setFixedSize(80, 50)
                btn.setStyleSheet("font-size: 16px;")
                btn.clicked.connect(lambda _, text=btn_text: self.on_button_click(text))
                grid.addWidget(btn, row, col)
                col += 1
            row += 1

        self.setLayout(layout)

    # --- 버튼 클릭 이벤트 처리 ---
    def on_button_click(self, text):
        if text == "AC":
            self.clear()
        elif text == "=":
            self.calculate()
        elif text == "sin":
            self.func_sin()
        elif text == "cos":
            self.func_cos()
        elif text == "tan":
            self.func_tan()
        elif text == "sinh":
            self.func_sinh()
        elif text == "cosh":
            self.func_cosh()
        elif text == "tanh":
            self.func_tanh()
        elif text == "π":
            self.func_pi()
        elif text == "x²":
            self.func_square()
        elif text == "x³":
            self.func_cube()
        else:
            self.append(text)

        # 결과를 디스플레이에 업데이트
        self.display.setText(self.get_display())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EngineeringCalculator()
    window.show()
    sys.exit(app.exec())
