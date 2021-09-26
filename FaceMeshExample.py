import cv2 as cv
import time
import FaceMeshModule as fm

cap = cv.VideoCapture(0)
pTime = 0
detector = fm.FaceMeshDetector()

while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img)

    if len(faces) != 0:
        print(faces)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    cv.imshow("Face Mesh", img)
    cv.waitKey(1)