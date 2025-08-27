# cctv.py
import os
import cv2

def show_people(folder="CCTV"):
    """CCTV 사진에서 사람을 찾아 화면에 출력하고 엔터 키로 다음 이미지 검색"""
    # 1. 폴더 내 이미지 목록 가져오기 (jpg, jpeg, png만)
    files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    files.sort()

    if not files:
        print("⚠️ 이미지 파일이 없습니다.")
        return

    # 2. 사람 검출용 Haar Cascade 로드 (전신)
    cascade_path = cv2.data.haarcascades + "haarcascade_fullbody.xml"
    if not os.path.exists(cascade_path):
        print("❌ Haar Cascade 파일을 찾을 수 없습니다.")
        return
    body_cascade = cv2.CascadeClassifier(cascade_path)

    idx = 0
    while idx < len(files):
        img_path = os.path.join(folder, files[idx])
        img = cv2.imread(img_path)

        if img is None:
            print(f"❌ 이미지를 읽을 수 없습니다: {img_path}")
            idx += 1
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(bodies) > 0:
            # 사람 검출 시 이미지에 사각형 표시
            for (x, y, w, h) in bodies:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("Detected People", img)
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


if __name__ == "__main__":
    show_people("CCTV")
