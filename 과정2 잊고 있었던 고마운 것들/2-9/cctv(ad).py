# cctv.py
import os
import zipfile
import cv2

def unzip_cctv(zip_path, extract_to="CCTV"):
    """CCTV.zip 압축을 풀어서 CCTV 폴더 생성"""
    if not os.path.exists(extract_to):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            print(f"✅ {zip_path} 압축 해제 완료 → {extract_to} 폴더 생성")
    else:
        print(f"📂 {extract_to} 폴더가 이미 존재합니다.")

def show_images(folder="CCTV"):
    """사진을 순서대로 보여주고 ← → 키로 이동"""
    # 이미지 파일 목록 정렬
    files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    files.sort()

    if not files:
        print("⚠️ 이미지 파일이 없습니다.")
        return

    idx = 0
    while True:
        img_path = os.path.join(folder, files[idx])
        img = cv2.imread(img_path)

        if img is None:
            print(f"❌ 이미지를 읽을 수 없습니다: {img_path}")
            break

        cv2.imshow("CCTV Viewer", img)
        print(f"📷 현재 이미지: {files[idx]}")

        key = cv2.waitKey(0) & 0xFF
        if key == 27:  # ESC
            break
        elif key == ord('d'):  # D → 다음 사진
            idx = (idx + 1) % len(files)
        elif key == ord('a'):  # A → 이전 사진
            idx = (idx - 1) % len(files)


    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 1. CCTV.zip 압축 풀기
    unzip_cctv("CCTV.zip", "CCTV")

    # 2. 이미지 뷰어 실행
    show_images("CCTV")
