import cv2 as cv
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "fingers"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

pTime = 0

detector = htm.handDetector(minDetection=0.75, maxHands=1)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img, False)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        fingers = []

        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)

        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (10, 200), 3, cv.FONT_HERSHEY_PLAIN, (255, 255, 255), 2)
    cv.imshow("Finger Counter", img)
    cv.waitKey(1)