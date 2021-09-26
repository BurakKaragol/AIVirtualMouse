import cv2 as cv
import time
import numpy as np
import HandTrackingModule as hm
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cameraWidth, cameraHeight = 640, 480

cap = cv.VideoCapture(0)
cap.set(3, cameraWidth)
cap.set(4, cameraHeight)
detector = hm.handDetector(maxHands=1, minDetection= 0.75)
pTime = 0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)
minVol = volRange[0]
maxVol = volRange[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img, False)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)

        cv.circle(img, (x1, y1), 4, (255, 0, 0), 3)
        cv.circle(img, (x2, y2), 4, (255, 0, 0), 3)
        cv.circle(img, (cx, cy), 4, (255, 0, 0), 3)
        cv.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

        #Hand range 50 300
        #volume range -65 0
        vol = np.interp(length, [10, 120], [minVol, maxVol])
        dispVol = np.interp(length, [10, 120], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)

        cv.putText(img, f'{str(int(dispVol))}%', (20, 70), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
        cv.rectangle(img, (20, 80), (50, 280), (255, 255, 255), 2)
        cv.rectangle(img, (20, int(280 - dispVol * 2)), (50, 280), (255, 255, 255), cv.FILLED)

        if length < 20:
            cv.circle(img, (cx, cy), 5, (0, 0, 255), cv.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    cv.imshow("Volume Hand Control", img)
    cv.waitKey(1)