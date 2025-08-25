# engineering_calculator.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout
)
from PyQt6.QtCore import Qt

class EngineeringCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone Engineering Calculator")
        self.setFixedSize(600, 400)  # 아이폰 가로 모드 크기 비슷하게
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # 출력창
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 24px; padding: 10px;")
        layout.addWidget(self.display)

        # 버튼 레이아웃
        grid = QGridLayout()
        layout.addLayout(grid)

        # 공학용 계산기 버튼 배열 (아이폰 가로 모드와 유사하게)
        buttons = [
            # 1행
            ["(", ")", "mc", "m+", "m-", "mr"],
            # 2행
            ["2nd", "x²", "x³", "xʸ", "eˣ", "10ˣ"],
            # 3행
            ["1/x", "²√x", "³√x", "ʸ√x", "ln", "log₁₀"],
            # 4행
            ["x!", "sin", "cos", "tan", "e", "EE"],
            # 5행
            ["Rad", "sinh", "cosh", "tanh", "π", "Rand"],
            # 6행 (기본 계산기 라인)
            ["AC", "+/-", "%", "÷"],
            # 7행
            ["7", "8", "9", "×"],
            # 8행
            ["4", "5", "6", "-"],
            # 9행
            ["1", "2", "3", "+"],
            # 10행
            ["0", ".", "="]
        ]

        # 버튼 생성 및 배치
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

    def on_button_click(self, text):
        """버튼 클릭 이벤트"""
        if text == "AC":
            self.display.setText("")
        elif text == "=":
            # 실제 계산 기능은 이번 과제에선 구현하지 않음
            self.display.setText("= 결과 표시 예정")
        else:
            current_text = self.display.text()
            new_text = current_text + text
            self.display.setText(new_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EngineeringCalculator()
    window.show()
    sys.exit(app.exec())
