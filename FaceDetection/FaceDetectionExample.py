import cv2 as cv
import time
import FaceDetectionModule as fm

cap = cv.VideoCapture(0)
pTime = 0
detector = fm.FaceDetector()

while True:
    success, img = cap.read()
    img, bboxs = detector.findFaces(img)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    cv.imshow("Face Detection", img)
    cv.waitKey(1)