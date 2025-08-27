# cctv.py

import os
import cv2

def show_people(folder='CCTV'):
    """CCTV 사진에서 사람을 찾아 화면에 출력하고 엔터 키로 다음 이미지 검색"""
    # 1. 폴더 내 이미지 목록 가져오기
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    files.sort()

    if not files:
        print('⚠️ 이미지 파일이 없습니다.')
        return

    # 2. OpenCV 사람 검출기 생성
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    for file in files:
        path = os.path.join(folder, file)
        img = cv2.imread(path)

        if img is None:
            print(f'⚠️ 이미지를 읽을 수 없습니다: {file}')
            continue

        # 3. 사람 검출
        rects, _ = hog.detectMultiScale(img, winStride=(8, 8), padding=(16, 16), scale=1.05)

        # 4. 검출된 사람 표시
        for (x, y, w, h) in rects:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 5. 이미지 화면에 출력
        cv2.imshow('CCTV People Detection', img)

        # 6. 엔터키를 누르면 다음 이미지로
        key = cv2.waitKey(0)
        if key == 13:  # 엔터키
            continue
        else:
            print('검색이 중단되었습니다.')
            break

    cv2.destroyAllWindows()
    print('✅ 모든 이미지 검색이 끝났습니다.')

if __name__ == '__main__':
    show_people()
