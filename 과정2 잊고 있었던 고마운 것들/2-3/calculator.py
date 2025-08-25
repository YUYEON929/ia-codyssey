# calculator.py
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout
from PyQt6.QtCore import Qt


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone Style Calculator")
        self.setFixedSize(320, 480)  # 아이폰 계산기 비율에 맞춰 크기 고정

        # --- 출력창 ---
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setStyleSheet("font-size: 28px; padding: 15px;")
        self.display.setText("0")

        # --- 버튼 배치 ---
        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        # 아이폰 계산기 버튼 순서
        buttons = [
            ["AC", "+/-", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        # 버튼 생성
        for row, row_values in enumerate(buttons):
            for col, text in enumerate(row_values):
                btn = QPushButton(text)
                btn.setFixedSize(70, 70)
                btn.setStyleSheet("font-size: 20px;")

                # '0' 버튼은 아이폰처럼 2칸 차지
                if text == "0":
                    self.grid.addWidget(btn, row + 1, col, 1, 2)
                else:
                    # '0' 다음 칸 보정
                    if row == 4 and col > 0:
                        self.grid.addWidget(btn, row + 1, col + 1)
                    else:
                        self.grid.addWidget(btn, row + 1, col)

                # 숫자/점 입력 이벤트 연결
                if text.isdigit() or text == ".":
                    btn.clicked.connect(lambda checked, val=text: self.num_pressed(val))
                else:
                    btn.clicked.connect(lambda checked, val=text: self.op_pressed(val))

        # 전체 레이아웃
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)
        main_layout.addLayout(self.grid)
        self.setLayout(main_layout)

    # --- 숫자 입력 이벤트 ---
    def num_pressed(self, val):
        if self.display.text() == "0":
            self.display.setText(val)
        else:
            self.display.setText(self.display.text() + val)

    # --- 연산 버튼 이벤트 ---
    def op_pressed(self, val):
        # 이번 과제에서는 계산 로직 불필요 → 입력만 표시
        self.display.setText(self.display.text() + " " + val + " ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CalculatorUI()
    win.show()
    sys.exit(app.exec())
