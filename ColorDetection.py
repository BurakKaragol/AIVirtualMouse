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
    
    lower_color_bound_1 = np.array([110, 50, 50]) #blue min
    upper_color_bound_1 = np.array([130, 255, 255]) #blue max
    lower_color_bound_2 = np.array([170, 50, 50]) #red min
    upper_color_bound_2 = np.array([190, 255, 255]) #red max
    lower_color_bound_3 = np.array([35, 50, 50]) #green min
    upper_color_bound_3 = np.array([75, 255, 255]) #green max
    lower_color_bound_4 = np.array([25, 50, 50]) #yellow min
    upper_color_bound_4 = np.array([30, 255, 255]) #yellow max
    
    mask_color_1 = cv.inRange(hsv, lower_color_bound_1, uupper_color_bound_1)
    mask_color_2 = cv.inRange(hsv, lower_color_bound_2, upper_color_bound_2)
    mask_color_3 = cv.inRange(hsv, lower_color_bound_3, upper_color_bound_3)
    mask_color_4 = cv.inRange(hsv, lower_color_bound_4, upper_color_bound_4)
    
    feat_color_1 = np.mean(mask_color_1)
    feat_color_2 = np.mean(mask_color_2)
    feat_color_3 = np.mean(mask_color_3)
    feat_color_4 = np.mean(mask_color_4)
    
    item_color_1 = cv.bitwise_and(cut, cut, mask = mask_color_1)
    item_color_2 = cv.bitwise_and(cut, cut, mask = mask_color_2)
    item_color_3 = cv.bitwise_and(cut, cut, mask = mask_color_3)
    item_color_4 = cv.bitwise_and(cut, cut, mask = mask_color_4)
    
    cv.putText(item_color_1, str(feat_colord_1), (50, 50), 1, 2,
               [255, 255, 255], 1)
    cv.putText(item_color_2, str(feat_color_2), (50, 50), 1, 2,
                [255, 255, 255], 1)
    cv.putText(item_color_3, str(feat_color_3), (50, 50), 1, 2,
               [255, 255, 255], 1)
    cv.putText(item_color_4, str(feat_color_4), (50, 50), 1, 2,
                [255, 255, 255], 1)
    
    if feat_color_1 > 1:
        cv.putText(img, 'blue', (10, 230), 2, 1, [255, 0, 0], 2)
        [x,y] = np.where(mask_color_1 == 255)
        x_m = np.mean(x).astype(np.uint8)
        y_m = np.mean(y).astype(np.uint8)
        x_diff = abs(x[0] - x[-1])
        y_diff = abs(y[0] - y[-1])
        average = (x_diff + y_diff) / 2
        img = cv.circle(img, (y_m, x_m), int(average),
                        (255, 0, 0), 3)
        cv.putText(img, 'Circle radius:: ' + str(average),
                   (10, 260), 1, 2, [255, 255, 255], 2)

    elif feat_color_2 > 1:
        cv.putText(img, 'red', (10, 230), 2, 1, [0, 0, 255], 2)
        [x,y] = np.where(mask_color_2 == 255)
        x_m = np.mean(x).astype(np.uint8)
        y_m = np.mean(y).astype(np.uint8)
        x_diff = abs(x[0] - x[-1])
        y_diff = abs(y[0] - y[-1])
        average = (x_diff + y_diff) / 2
        img = cv.circle(img, (y_m, x_m), int(average),
                        (0, 0, 255), 3)
        cv.putText(img, 'Circle radius:: ' + str(average),
                   (10, 260), 1, 2, [255, 255, 255], 2)

    elif feat_color_3 > 1:
        cv.putText(img, 'green', (10, 230), 2, 1, [0, 255, 0], 2)
        [x,y] = np.where(mask_color_3 == 255)
        x_m = np.mean(x).astype(np.uint8)
        y_m = np.mean(y).astype(np.uint8)
        x_diff = abs(x[0] - x[-1])
        y_diff = abs(y[0] - y[-1])
        average = (x_diff + y_diff) / 2
        img = cv.circle(img, (y_m, x_m), int(average),
                        (0, 255, 0), 3)
        cv.putText(img, 'Circle radius:: ' + str(average),
                   (10, 260), 1, 2, [255, 255, 255], 2)

    elif feat_color_4 > 1:
        cv.putText(img, 'yellow', (10, 230), 2, 1, [0, 255, 255], 2)
        [x,y] = np.where(mask_color_4 == 255)
        x_m = np.mean(x).astype(np.uint8)
        y_m = np.mean(y).astype(np.uint8)
        x_diff = abs(x[0] - x[-1])
        y_diff = abs(y[0] - y[-1])
        average = (x_diff + y_diff) / 2
        img = cv.circle(img, (y_m, x_m), int(average),
                        (0, 255, 255), 3)
        cv.putText(img, 'Circle radius:: ' + str(average),
                   (10, 260), 1, 2, [255, 255, 255], 2)

    else:
        cv.putText(img, 'color Yok', (10, 230), 2, 1, [255, 255, 255], 2)
    
    cv.imshow('orjinal', img)
    cv.imshow('cut', cut)
    cv.imshow('hsv', hsv)
    cv.imshow('blue mask', mask_color_1)
    cv.imshow('red mask', mask_color_2)
    cv.imshow('green mask', mask_color_3)
    cv.imshow('yellow mask', mask_color_4)
    cv.imshow('blue item', item_color_1)
    cv.imshow('red item', item_color_2)
    cv.imshow('green item', item_color_3)
    cv.imshow('yellow item', item_color_4)
    
    
    k = cv.waitKey(5)
    if k == 27: #press ESC to close app
        break

cap.release()
cv.destroyAllWindows()
