import cv2
import mediapipe as mp
import time


class poseDetector():
    # 내부에는 첫 번째 클래스가 있다고 말할 것임

    def __init__(self, mode = False,  upBody = False, smooth = True,
                 detectionCon = 0.5, trackCon=0.5):
        # 첫번째 매개변수가 mode니까 다음과 같이 유지
        # [ 빠른 탐지를 위해 false, 상체 작성하기 위해 false, 부드러움 T,
        # 감지 신뢰도는 0.5, 추적 신뢰도는 0.5 ]
        # [ ] : 하이퍼파라미터 => 입력함으로써 아래 5줄은 제거 가능

        self.mode = mode
        # 우리가 생성할 때마다 새로운 객체는 자체 변수를 가질 것이라는 것
        # self.을 쓸 때마다, 그것은 객체의 변수
        # 클래스 내에서 변수를 사용할 때마다 우리는 self.을 쓸 것임
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon           # 신뢰 추적

        # static_image_mode = False,
        # upper_body_only = False,
        # smooth_landmark = True,
        # min_detection_confidence = 0.5,
        # min_tracking_confidence = 0.5):

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, 1, self.upBody, self.smooth, False,
                                     self.detectionCon, self.trackCon) # 모든 매개변수를 전송해야 하므로


        # pose를 찾는 메서드를 만들어 보자
    def findPose(self, img, draw = True):
        # 새 객체를 만들때마다 셀을 작성해야 하고, 이미지를 제공해야함, draw라는 플래그도 갖게 되고, 이를 ture로 설정
        # 사용자에게 그리고 싶은지 or 당신이 그것을 이미지에 표시하고 싶은지 여부 물을 것임

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(imgRGB)
        # print(results.pose_landmarks)

        if results.pose_landmarks:
            if draw:  # 플래그를 넣어야 함
                self.mpDraw.draw_landmarks(img, results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
                # 랜드마크가 무엇을 표시하는 것일까 (x,y,z)
                # 프로세스 및 자체 도트 mp그리기 다음, 또한 쓸 수 있음
        return img

            # for id, lm in enumerate(results.pose_landmarks.landmark):
            #     h, w, c = img.shape
            #     print(id, lm)
            # lm을 쓰면 무슨일이 일어나는지 볼 수 있고, id번호도 인쇄할 수 있음
            # (여기서 정확히 무엇을 추출하는지 알 수 있음)
            # 33개의 랜드마크가 모두 있음
            # 실제 픽셀값을 얻는 것이 가능
            # cx, cy = int(lm.x*w), int(lm.y*h)
            # x좌표*너비, y좌표*높이
            # cv2.circle(img, (cx,cy), 5, (255,0,0), cv2.FILLED)
            # 5는 점의 크기 // (255,0,0)은 색깔
            # 직접 넣은 파란색 점이 있는 것을 볼 수 있음
            # 올바른 픽셀값에서, 올바른 정보를 얻고 있다는 것을 알 수 있음



    # 원하는 번호를 집어서 달라고 하면 될 듯
    # 제스처 인식 등에 사용
    # 이 객체 내에서 정보를 추출하는 방법

def main():
    cap = cv2.VideoCapture('test.mp4')  # 경로에 'test.mp4' 파일 넣어주고 실행할 것
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)  # 포즈를 찾으면 img를 주고

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (78, 58), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255,0,0),3)

        cv2.imshow('Image', img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()   # 이것을 단독으로 실행하는 경우, main을 실행한다는 것
             # 함수 및 다른 함수를 호출하는 경우, 이 부분을 실행하지 않음


# 클래스 생성 -> 객체를 생성하려면 포즈를 감지하고, 이 모든 점을 찾을 수 있는 메서드를 가질 수 있어야 함
