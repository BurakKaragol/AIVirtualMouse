import cv2 as cv
import time
import HandTrackingModule as htm

pTime = 0
cTime = 0
cap = cv.VideoCapture(0)
detector = htm.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    # if len(lmList) != 0:
        # print(lmList[0])

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

    cv.imshow("Hand Tracking", img)
    cv.waitKey(1)