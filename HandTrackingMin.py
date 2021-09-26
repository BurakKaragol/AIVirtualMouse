import cv2 as cv
import numpy as np
import mediapipe as mp
import time

cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    p1x, p1y, p2x, p2y, distance = 0, 0, 0, 0, 0

    if results.multi_hand_landmarks:
        for handLandmark in results.multi_hand_landmarks:
            for id, lm in enumerate(handLandmark.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                if id == 4:
                    # cv.circle(img, (cx, cy), 25, (0, 0, 255), cv.FILLED)
                    p1x, p1y = cx, cy
                if id == 8:
                    # cv.circle(img, (cx, cy), 15, (255, 255, 255), cv.FILLED)
                    p2x, p2y = cx, cy

            mpDraw.draw_landmarks(img, handLandmark, mpHands.HAND_CONNECTIONS)

    xDistance = abs(p1x - p2x)
    yDistance = abs(p1y - p2y)
    distance = np.sqrt(pow(xDistance, 2) + (pow(yDistance, 2)))
    xMid, yMid = 0, 0
    if p1x < p2x:
        xMid = p1x + xDistance / 2
    else:
        xMid = p2x + xDistance / 2
    if p1y < p2y:
        yMid = p1y + yDistance / 2
    else:
        yMid = p2y + yDistance / 2
    # cv.line(img, (p1x, p1y), (p2x, p2y), (0, 0, 255))
    # cv.circle(img, (int(xMid), int(yMid)), int(distance / 2), (0, 255, 0), 2)
    # cv.putText(img, str(int(distance)), (10, 100), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

    cv.imshow("Hand Tracking", img)
    cv.waitKey(1)