import cv2
import os
import numpy as np
import csv
from datetime import datetime

# -------------------------
# 1. 얼굴 등록용 폴더
# -------------------------
faces_dir = os.path.join(os.path.dirname(__file__), "faces")
if not os.path.exists(faces_dir):
    os.makedirs(faces_dir)
    print("faces 폴더 생성됨, 사진을 넣고 다시 실행하세요.")
    exit()

# -------------------------
# 2. 학습용 데이터 준비 (한글 경로 지원)
# -------------------------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = []
labels = []
label_id = 0
names = {}

def imread_unicode(path):
    """한글 경로 이미지 읽기"""
    stream = open(path, "rb").read()
    np_arr = np.frombuffer(stream, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

for file in os.listdir(faces_dir):
    if file.lower().endswith((".jpg", ".png")):
        path = os.path.join(faces_dir, file)
        img = imread_unicode(path)
        if img is None:
            print(f"❌ 이미지 읽기 실패: {file}")
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected = face_cascade.detectMultiScale(gray, 1.1, 5)
        if len(detected) == 0:
            print(f"⚠️ 얼굴 못 찾음: {file}")
            continue
        x, y, w, h = detected[0]  # 첫 번째 얼굴만
        face_roi = gray[y:y+h, x:x+w]
        face_resized = cv2.resize(face_roi, (200, 200))
        faces.append(face_resized)
        labels.append(label_id)
        name = os.path.splitext(file)[0]
        names[label_id] = name
        label_id += 1

if len(faces) == 0:
    print("❌ 학습할 얼굴 데이터가 없습니다. faces 폴더 확인하세요.")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))
print("✅ 얼굴 학습 완료:", names)

# -------------------------
# 3. 출석 CSV 파일 준비
# -------------------------
filename = "출석.csv"
if not os.path.exists(filename):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["이름", "날짜", "시간"])

# -------------------------
# 4. 웹캠 실행 & 출석 체크
# -------------------------
cap = cv2.VideoCapture(0)
print("🎥 웹캠 시작, 얼굴을 보여주세요. 종료: q 키")

while True:
    ret, frame = cap.read()
    if not ret:
        print("카메라 오류")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_detected = face_cascade.detectMultiScale(gray_frame, 1.1, 5)

    if len(faces_detected) == 0:
        cv2.putText(frame, "얼굴 감지 실패", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        for (x, y, w, h) in faces_detected:
            face_img = gray_frame[y:y+h, x:x+w]
            face_resized = cv2.resize(face_img, (200, 200))
            label_id, confidence = recognizer.predict(face_resized)

            if confidence < 80:
                name = names[label_id]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # 출석 기록
                now = datetime.now()
                date = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M:%S")

                with open(filename, "r", encoding="utf-8-sig") as f:
                    lines = f.readlines()
                names_in_file = [line.split(",")[0] for line in lines[1:]]
                if name not in names_in_file:
                    with open(filename, "a", newline="", encoding="utf-8-sig") as f:
                        writer = csv.writer(f)
                        writer.writerow([name, date, time_str])
                    print(f"{name} 출석 완료: {date} {time_str}")
            else:
                cv2.putText(frame, "등록되지 않은 얼굴", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("출석부", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
