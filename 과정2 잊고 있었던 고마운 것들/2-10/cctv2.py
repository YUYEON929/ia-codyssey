from ultralytics import YOLO
import cv2, os

def show_people(folder="CCTV"):
    files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    files.sort()
    if not files:
        print("⚠️ 이미지 파일이 없습니다.")
        return

    model = YOLO("yolov8n.pt")  # 작은 YOLOv8 모델

    idx = 0
    while idx < len(files):
        img_path = os.path.join(folder, files[idx])
        img = cv2.imread(img_path)
        if img is None:
            print(f"❌ 이미지를 읽을 수 없습니다: {img_path}")
            idx += 1
            continue

        results = model(img, classes=[0])  # class 0 = person
        annotated = results[0].plot()

        if len(results[0].boxes) > 0:
            cv2.imshow("Detected People", annotated)
            print(f"📷 사람 발견: {files[idx]} - 엔터 키를 눌러 다음 이미지 검색")
            while True:
                key = cv2.waitKeyEx(0)
                if key == 13:  # 엔터
                    break
        else:
            print(f"❌ 사람 없음: {files[idx]}")

        idx += 1

    print("✅ 모든 이미지 검색 완료")
    cv2.destroyAllWindows()
