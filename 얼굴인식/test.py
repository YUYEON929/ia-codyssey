import cv2
import os
import numpy as np

faces_dir = r"c:\Users\apple\OneDrive\바탕 화면\codyssey\얼굴인식\faces"
labels = []
faces = []
names = {}

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

label_id = 0
for file in os.listdir(faces_dir):
    if file.endswith(".jpg") or file.endswith(".png"):
        path = os.path.join(faces_dir, file)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        detected = face_cascade.detectMultiScale(img, 1.1, 5)

        for (x, y, w, h) in detected:
            face = img[y:y+h, x:x+w]
            faces.append(face)
            labels.append(label_id)
        names[label_id] = os.path.splitext(file)[0]
        label_id += 1

# LBPH 모델 학습
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))
recognizer.save("trainer.yml")

# 이름 매핑 저장
import pickle
with open("names.pkl", "wb") as f:
    pickle.dump(names, f)

print("✅ 얼굴 등록 완료:", names)
