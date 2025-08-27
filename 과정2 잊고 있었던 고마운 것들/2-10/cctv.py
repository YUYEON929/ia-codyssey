# cctv_optimized.py

import os
import cv2
import numpy as np

def non_max_suppression(boxes, overlapThresh=0.65):
    """겹치는 박스를 제거하는 Non-Maximum Suppression"""
    if len(boxes) == 0:
        return []

    boxes = np.array(boxes)
    pick = []

    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,0] + boxes[:,2]
    y2 = boxes[:,1] + boxes[:,3]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    while len(idxs) > 0:
        last = idxs[-1]
        pick.append(last)
        idxs = idxs[:-1]

        xx1 = np.maximum(x1[last], x1[idxs])
        yy1 = np.maximum(y1[last], y1[idxs])
        xx2 = np.minimum(x2[last], x2[idxs])
        yy2 = np.minimum(y2[last], y2[idxs])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        overlap = (w * h) / area[idxs]

        idxs = idxs[overlap <= overlapThresh]

    return boxes[pick].astype("int")

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

        # 3. 전처리 (흑백 변환 + 히스토그램 평활화)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        # 4. 사람 검출 (파라미터 튜닝)
        rects, _ = hog.detectMultiScale(
            gray,
            winStride=(4, 4),
            padding=(8, 8),
            scale=1.03
        )

        # 5. NMS 적용
        rects = non_max_suppression(rects, overlapThresh=0.65)

        # 6. 검출된 사람 표시
        for (x, y, w, h) in rects:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 7. 이미지 화면에 출력
        cv2.imshow('CCTV People Detection', img)

        # 8. 엔터키를 누르면 다음 이미지로
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
