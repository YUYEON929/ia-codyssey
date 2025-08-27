# calculator.py
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout,
                             QPushButton, QLineEdit)
from PyQt6.QtCore import Qt


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Calculator")
        self.resize(300, 400)

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

        # 아이폰 계산기와 같은 버튼 배치
        buttons = [
            ("C", 0, 0), ("+/-", 0, 1), ("%", 0, 2), ("÷", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("×", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
            ("0", 4, 0, 1, 2), (".", 4, 2), ("=", 4, 3),
        ]

        # 버튼 생성 및 배치
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
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec())
