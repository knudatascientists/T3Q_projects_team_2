import cv2
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture('test.mp4')
pTime = 0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        # 랜드마크가 무엇을 표시하는 것일까 (x,y,z)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            print(id, lm)
            # lm을 쓰면 무슨일이 일어나는지 볼 수 있고, id번호도 인쇄할 수 있음
            # (여기서 정확히 무엇을 추출하는지 알 수 있음)
            # 33개의 랜드마크가 모두 있음
            # 실제 픽셀값을 얻는 것이 가능
            cx, cy = int(lm.x*w), int(lm.y*h)
            # x좌표*너비, y좌표*높이
            cv2.circle(img, (cx,cy), 5, (255,0,0), cv2.FILLED)
            # 5는 점의 크기 // (255,0,0)은 색깔
            # 직접 넣은 파란색 점이 있는 것을 볼 수 있음
            # 올바른 픽셀값에서, 올바른 정보를 얻고 있다는 것을 알 수 있음

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (78, 58), cv2.FONT_HERSHEY_PLAIN, 3,
                (255,0,0),3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)

    # 원하는 번호를 집어서 달라고 하면 될 듯
    # 제스처 인식 등에 사용
    # 이 객체 내에서 정보를 추출하는 방법

