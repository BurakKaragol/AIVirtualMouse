import cv2 as cv
import mediapipe as mp
import time
import math

class poseDetector():
    def __init__(self, mode = False, complexity = 1, smoothLm = True, segmentation = False, smoothSegm = True,
                 minDetection = 0.5, minTracking = 0.5):
        self.mode = mode
        self.complexity = complexity
        self.smoothLm = smoothLm
        self.segmentation = segmentation
        self.smoothSegm = smoothSegm
        self.minDetection = minDetection
        self.minTracking = minTracking

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smoothLm, self.segmentation, self.smoothSegm,
                                     self.minDetection, self.minTracking)
        self.mpDraw = mp.solutions.drawing_utils

    def findPose(self, img, draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw = False):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv.putText(img, str(id), (cx, cy), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw = True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        angle =  abs(math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)))

        if draw:
            cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), 1)
            cv.line(img, (x2, y2), (x3, y3), (255, 255, 255), 1)
            cv.circle(img, (x1, y1), 5, (0, 0, 255), cv.FILLED)
            cv.circle(img, (x1, y1), 10, (255, 0, 0), 2)
            cv.circle(img, (x2, y2), 5, (0, 0, 255), cv.FILLED)
            cv.circle(img, (x2, y2), 10, (255, 0, 0), 2)
            cv.circle(img, (x3, y3), 5, (0, 0,255), cv.FILLED)
            cv.circle(img, (x3, y3), 10, (255, 0, 0), 2)
            cv.putText(img, str(int(angle)), (x2 + 20, y2 - 20), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

        return angle

def main():
    cap = cv.VideoCapture(0)
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv.putText(img, str(int(fps)), (20, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        cv.imshow("Pose Estimation", img)
        cv.waitKey(1)

if __name__ == "__main__":
    main()