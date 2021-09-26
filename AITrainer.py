import cv2 as cv
import numpy as np
import time
import PoseEstimationModule as pem

cap = cv.VideoCapture(0)
pTime = 0
count = 0
dir = 0
detector = pem.poseDetector()

while True:
    success, img = cap.read()
    img = detector.findPose(img, draw=False)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        angle = detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle, [45, 145], [0, 100])
        color = np.interp(angle, [45, 145], [0, 255])

        cv.rectangle(img, (29, 89), (51, 291), (255, 255, 255), 2)
        cv.rectangle(img, (30, 90 + int(per) * 2), (50, 290), (0, 255 - int(color), int(color)), cv.FILLED)

        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0

        cv.putText(img, str(count), (30, 80), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
        #str(int(count)) 1 er 1 er sayar

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    cv.imshow("AI Trainer", img)
    cv.waitKey(1)