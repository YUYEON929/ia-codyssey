# calculator.py
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout,
                             QPushButton, QLineEdit)
from PyQt6.QtCore import Qt


class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_input = "0"   # 현재 입력된 수
        self.operator = None       # 연산자
        self.operand = None        # 이전 값

    def input_number(self, num: str):
        if self.current_input == "0" and num != ".":
            self.current_input = num
        else:
            # 소수점 중복 방지
            if num == "." and "." in self.current_input:
                return
            self.current_input += num

    def set_operator(self, op: str):
        if self.operator and self.operand is not None:
            self.equal()
        self.operand = float(self.current_input)
        self.operator = op
        self.current_input = "0"

    def add(self):
        return self.operand + float(self.current_input)

    def subtract(self):
        return self.operand - float(self.current_input)

    def multiply(self):
        return self.operand * float(self.current_input)

    def divide(self):
        try:
            return self.operand / float(self.current_input)
        except ZeroDivisionError:
            return "Error"

    def equal(self):
        if self.operator is None or self.operand is None:
            return self.current_input
        if self.operator == "+":
            result = self.add()
        elif self.operator == "-":
            result = self.subtract()
        elif self.operator == "×":
            result = self.multiply()
        elif self.operator == "÷":
            result = self.divide()
        else:
            result = self.current_input

        self.current_input = str(result)
        self.operator = None
        self.operand = None
        return self.current_input

    def negative_positive(self):
        if self.current_input.startswith("-"):
            self.current_input = self.current_input[1:]
        else:
            if self.current_input != "0":
                self.current_input = "-" + self.current_input

    def percent(self):
        value = float(self.current_input) / 100
        self.current_input = str(value)


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calc = Calculator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Calculator")
        self.resize(300, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 24px; padding: 10px;")
        layout.addWidget(self.display)

        grid = QGridLayout()
        layout.addLayout(grid)

        buttons = [
            ("C", 0, 0), ("+/-", 0, 1), ("%", 0, 2), ("÷", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("×", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
            ("0", 4, 0, 1, 2), (".", 4, 2), ("=", 4, 3),
        ]

        for text, row, col, *span in buttons:
            button = QPushButton(text)
            button.setFixedHeight(60)
            button.setStyleSheet("font-size: 18px;")
            if span:
                grid.addWidget(button, row, col, span[0], span[1])
            else:
                grid.addWidget(button, row, col)

            button.clicked.connect(lambda _, t=text: self.on_button_click(t))

    def on_button_click(self, text):
        if text.isdigit() or text == ".":
            self.calc.input_number(text)
        elif text in ["+", "-", "×", "÷"]:
            self.calc.set_operator(text)
        elif text == "=":
            self.calc.equal()
        elif text == "C":
            self.calc.reset()
        elif text == "+/-":
            self.calc.negative_positive()
        elif text == "%":
            self.calc.percent()

        self.display.setText(self.calc.current_input)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec())
