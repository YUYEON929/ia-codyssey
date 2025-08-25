# calculator.py
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout
from PyQt6.QtCore import Qt


# --- 계산 기능 담당 클래스 ---
class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current = "0"   # 현재 입력 중인 값
        self.operator = None # 선택된 연산자
        self.operand = None  # 이전에 입력된 값
        return self.current

    def input_number(self, num):
        if self.current == "0":
            self.current = num
        else:
            self.current += num
        return self.current

    def input_dot(self):
        if "." not in self.current:
            self.current += "."
        return self.current

    def set_operator(self, op):
        if self.operator is not None:
            self.equal()
        self.operand = float(self.current)
        self.operator = op
        self.current = "0"
        return str(self.operand)

    def add(self, x, y): return x + y
    def subtract(self, x, y): return x - y
    def multiply(self, x, y): return x * y
    def divide(self, x, y):
        if y == 0:
            return "Error"
        return x / y

    def negative_positive(self):
        if self.current.startswith("-"):
            self.current = self.current[1:]
        else:
            if self.current != "0":
                self.current = "-" + self.current
        return self.current

    def percent(self):
        try:
            self.current = str(float(self.current) / 100)
        except:
            self.current = "Error"
        return self.current

    def equal(self):
        if self.operator is None or self.operand is None:
            return self.current
        try:
            x = self.operand
            y = float(self.current)
            if self.operator == "+": result = self.add(x, y)
            elif self.operator == "-": result = self.subtract(x, y)
            elif self.operator == "×": result = self.multiply(x, y)
            elif self.operator == "÷": result = self.divide(x, y)
            else: result = y
            self.current = str(result)
            self.operator = None
            self.operand = None
        except:
            self.current = "Error"
        return self.current


# --- UI 담당 클래스 ---
class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone Style Calculator")
        self.setFixedSize(320, 480)

        self.calc = Calculator()  # 계산 로직 객체

        # --- 출력창 ---
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setStyleSheet("font-size: 28px; padding: 15px;")

        # --- 버튼 배치 ---
        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        buttons = [
            ["AC", "+/-", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        for row, row_values in enumerate(buttons):
            for col, text in enumerate(row_values):
                btn = QPushButton(text)
                btn.setFixedSize(70, 70)
                btn.setStyleSheet("font-size: 20px;")

                # '0' 버튼은 2칸 차지
                if text == "0":
                    self.grid.addWidget(btn, row + 1, col, 1, 2)
                else:
                    if row == 4 and col > 0:
                        self.grid.addWidget(btn, row + 1, col + 1)
                    else:
                        self.grid.addWidget(btn, row + 1, col)

                # 이벤트 연결
                if text.isdigit():
                    btn.clicked.connect(lambda checked, val=text: self.num_pressed(val))
                elif text == ".":
                    btn.clicked.connect(self.dot_pressed)
                elif text in ["+", "-", "×", "÷"]:
                    btn.clicked.connect(lambda checked, val=text: self.op_pressed(val))
                elif text == "=":
                    btn.clicked.connect(self.equal_pressed)
                elif text == "AC":
                    btn.clicked.connect(self.reset_pressed)
                elif text == "+/-":
                    btn.clicked.connect(self.neg_pressed)
                elif text == "%":
                    btn.clicked.connect(self.percent_pressed)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)
        main_layout.addLayout(self.grid)
        self.setLayout(main_layout)

    # --- 이벤트 핸들러 ---
    def num_pressed(self, val):
        self.display.setText(self.calc.input_number(val))

    def dot_pressed(self):
        self.display.setText(self.calc.input_dot())

    def op_pressed(self, op):
        self.display.setText(self.calc.set_operator(op))

    def equal_pressed(self):
        self.display.setText(self.calc.equal())

    def reset_pressed(self):
        self.display.setText(self.calc.reset())

    def neg_pressed(self):
        self.display.setText(self.calc.negative_positive())

    def percent_pressed(self):
        self.display.setText(self.calc.percent())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CalculatorUI()
    win.show()
    sys.exit(app.exec())
