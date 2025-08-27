# engineering_calculator.py
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout,
                             QPushButton, QLineEdit)
from PyQt6.QtCore import Qt


class EngineeringCalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
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
        """버튼을 누르면 디스플레이에 표시"""
        current = self.display.text()
        if current == "0":
            if text.isdigit() or text == ".":
                self.display.setText(text)
            else:
                self.display.setText(current + text)
        else:
            self.display.setText(current + text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EngineeringCalculatorUI()
    window.show()
    sys.exit(app.exec())
