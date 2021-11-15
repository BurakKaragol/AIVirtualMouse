import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

cap = cv.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    img = cv.flip(frame, 1)
    img = cv.rectangle(img, (0,0), (200, 200), (0, 0, 255), 2)
    cut = img[0:200, 0:200, :]
    hsv = cv.cvtColor(cut, cv.COLOR_BGR2HSV)
    
    alt_renk1 = np.array([110, 50, 50]) #mavi min
    ust_renk1 = np.array([130, 255, 255]) #mavi max
    alt_renk2 = np.array([170, 50, 50]) #kirmizi min
    ust_renk2 = np.array([190, 255, 255]) #kirmizi max
    alt_renk3 = np.array([35, 50, 50]) #yesil min
    ust_renk3 = np.array([75, 255, 255]) #yesil max
    alt_renk4 = np.array([25, 50, 50]) #sari min
    ust_renk4 = np.array([30, 255, 255]) #sari max
    
    mask_renk1 = cv.inRange(hsv, alt_renk1, ust_renk1)
    mask_renk2 = cv.inRange(hsv, alt_renk2, ust_renk2)
    mask_renk3 = cv.inRange(hsv, alt_renk3, ust_renk3)
    mask_renk4 = cv.inRange(hsv, alt_renk4, ust_renk4)
    
    feat_renk1 = np.mean(mask_renk1)
    feat_renk2 = np.mean(mask_renk2)
    feat_renk3 = np.mean(mask_renk3)
    feat_renk4 = np.mean(mask_renk4)
    
    item_renk1 = cv.bitwise_and(cut, cut, mask = mask_renk1)
    item_renk2 = cv.bitwise_and(cut, cut, mask = mask_renk2)
    item_renk3 = cv.bitwise_and(cut, cut, mask = mask_renk3)
    item_renk4 = cv.bitwise_and(cut, cut, mask = mask_renk4)
    
    cv.putText(item_renk1, str(feat_renk1), (50, 50), 1, 2,
               [255, 255, 255], 1)
    cv.putText(item_renk2, str(feat_renk2), (50, 50), 1, 2,
                [255, 255, 255], 1)
    cv.putText(item_renk3, str(feat_renk3), (50, 50), 1, 2,
               [255, 255, 255], 1)
    cv.putText(item_renk4, str(feat_renk4), (50, 50), 1, 2,
                [255, 255, 255], 1)
    
    if feat_renk1 > 1:
        cv.putText(img, 'Mavi', (10, 230), 2, 1, [255, 0, 0], 2)
        [x,y] = np.where(mask_renk1 == 255)
        x_m = np.mean(x).astype(np.uint8)
        y_m = np.mean(y).astype(np.uint8)
        x_fark = abs(x[0] - x[-1])
        y_fark = abs(y[0] - y[-1])
        ortalama = (x_fark + y_fark) / 2
        img = cv.circle(img, (y_m, x_m), int(ortalama),
                        (255, 0, 0), 3)
        cv.putText(img, 'Cember capi: ' + str(ortalama),
                   (10, 260), 1, 2, [255, 255, 255], 2)

    elif feat_renk2 > 1:
        cv.putText(img, 'Kirmizi', (10, 230), 2, 1, [0, 0, 255], 2)
        [x,y] = np.where(mask_renk2 == 255)
        x_m = np.mean(x).astype(np.uint8)
        y_m = np.mean(y).astype(np.uint8)
        x_fark = abs(x[0] - x[-1])
        y_fark = abs(y[0] - y[-1])
        ortalama = (x_fark + y_fark) / 2
        img = cv.circle(img, (y_m, x_m), int(ortalama),
                        (0, 0, 255), 3)
        cv.putText(img, 'Cember capi: ' + str(ortalama),
                   (10, 260), 1, 2, [255, 255, 255], 2)

    elif feat_renk3 > 1:
        cv.putText(img, 'Yesil', (10, 230), 2, 1, [0, 255, 0], 2)
        [x,y] = np.where(mask_renk3 == 255)
        x_m = np.mean(x).astype(np.uint8)
        y_m = np.mean(y).astype(np.uint8)
        x_fark = abs(x[0] - x[-1])
        y_fark = abs(y[0] - y[-1])
        ortalama = (x_fark + y_fark) / 2
        img = cv.circle(img, (y_m, x_m), int(ortalama),
                        (0, 255, 0), 3)
        cv.putText(img, 'Cember capi: ' + str(ortalama),
                   (10, 260), 1, 2, [255, 255, 255], 2)

    elif feat_renk4 > 1:
        cv.putText(img, 'Sari', (10, 230), 2, 1, [0, 255, 255], 2)
        [x,y] = np.where(mask_renk4 == 255)
        x_m = np.mean(x).astype(np.uint8)
        y_m = np.mean(y).astype(np.uint8)
        x_fark = abs(x[0] - x[-1])
        y_fark = abs(y[0] - y[-1])
        ortalama = (x_fark + y_fark) / 2
        img = cv.circle(img, (y_m, x_m), int(ortalama),
                        (0, 255, 255), 3)
        cv.putText(img, 'Cember capi: ' + str(ortalama),
                   (10, 260), 1, 2, [255, 255, 255], 2)

    else:
        cv.putText(img, 'Renk Yok', (10, 230), 2, 1, [255, 255, 255], 2)
    
    cv.imshow('orjinal', img)
    cv.imshow('cut', cut)
    cv.imshow('hsv', hsv)
    cv.imshow('blue mask', mask_renk1)
    cv.imshow('red mask', mask_renk2)
    cv.imshow('green mask', mask_renk3)
    cv.imshow('yellow mask', mask_renk4)
    cv.imshow('blue item', item_renk1)
    cv.imshow('red item', item_renk2)
    cv.imshow('green item', item_renk3)
    cv.imshow('yellow item', item_renk4)
    
    
    k = cv.waitKey(5)
    if k == 27: #ESC tusuna basildiginda donguden cikar
        break

cap.release()
cv.destroyAllWindows()
