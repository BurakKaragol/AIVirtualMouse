import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0)
pTime = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()
drawSpecs = mpDraw.DrawingSpec(thickness = 1, circle_radius = 2)

while True:
    success, img = cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpecs, drawSpecs)
            for id, lm in enumerate(faceLms.landmark):
                # print(id, lm)
                ih, iw, ic = img.shape
                x, y = int(lm.x * iw), int(lm.y * ih)
                print(id, x, y)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    cv.imshow("Face Mesh", img)
    cv.waitKey(1)