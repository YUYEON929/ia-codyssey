import cv2
import csv
from datetime import datetime
import os

# -------------------------
# 1. 얼굴 인식용 준비
# -------------------------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 예시: 이름과 얼굴 이미지 파일 연결 (여기선 단순히 한 명만 예제)
known_face_name = "홍길동"  # 감지 시 표시할 이름

# -------------------------
# 2. CSV 파일 준비
# -------------------------
filename = '출석.csv'
if not os.path.exists(filename):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['이름', '날짜', '시간'])

# -------------------------
# 3. 웹캠 시작
# -------------------------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("카메라를 가져올 수 없습니다.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        cv2.putText(frame, "얼굴 감지 실패", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, known_face_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # -------------------------
            # 4. 출석 기록 저장
            # -------------------------
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M:%S")

            # 기존 기록 확인 후 중복 방지
            with open(filename, 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()
            names_in_file = [line.split(',')[0] for line in lines[1:]]
            if known_face_name not in names_in_file:
                with open(filename, 'a', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow([known_face_name, date, time])
                print(f"{known_face_name} 출석 기록 완료: {date} {time}")

    cv2.imshow('출석부', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # q 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()
