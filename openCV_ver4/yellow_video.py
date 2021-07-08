import cv2 as cv
from collections import deque
import numpy as np
import imutils
import time

cap = cv.VideoCapture(1)
time.sleep(1.0)

lower_yellow = (30 - 10, 30, 30)
upper_yellow = (30 + 10, 255, 255)
wait_2sec = 1
ball_last_pos_x = 0
ball_last_pos_y = 0

while (True):
    ball_inside_field = 1

    video_color = cv.imread('http://192.168.66.1:9527/videostream.cgi?loginuse=admin&loginpas=admin')

    if wait_2sec == 1:
        time.sleep(2.0)
        wait_2sec = 0

    # resize
    ret, video_color = cap.read()
    height, width = video_color.shape[:2]

    video_color = cv.resize(video_color, (width, height), interpolation=cv.INTER_AREA)

    x1 = 30
    x2 = 440
    y1 = 110
    y2 = 530

    video_color = video_color[x1:x2, y1:y2].copy()

    # 블러 처리
    blurred = cv.GaussianBlur(video_color, (11, 11), 0)

    # 원본 영상을 HSV 영상으로 변환합니다.
    img_hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

    # 노란색 mask 씌우고 작은 무늬들(blob)을 지우기 위한 작업 수행
    img_mask = cv.inRange(img_hsv, lower_yellow, upper_yellow)
    img_mask = cv.erode(img_mask, None, iterations = 2)
    img_mask = cv.dilate(img_mask, None, iterations = 2)

    #mask의 윤곽 찾고 공의 중앙 x,y 초기화
    cnts = cv.findContours(img_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    #윤곽을 찾은 경우에만 수행
    if len(cnts) > 0:
        ball_inside_field = 1
        #마스크의 가장 큰 윤곽 찾고, 원을 찾는데 이용
        c = max(cnts, key=cv.contourArea)
        ((x,y), radius) = cv.minEnclosingCircle(c)
        M = cv.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        ball_last_pos_x = int( M["m10"] / M["m00"] )
        ball_last_pos_y = int( M["m01"] / M["m00"] )

        #반지름이 최소 사이즈인 경우에만 수행
        if radius > 10:
            # 원과 원의 중심을 프레임에 그리기
            cv.circle(video_color, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv.circle(video_color, center, 5, (0, 0, 255), -1)
    else:
        ball_inside_field = 0


    if ball_inside_field == 0:
        if ball_last_pos_x < 4 and ball_last_pos_x != 0 :
            print("right win!")
        elif ball_last_pos_x > 405 :
            print("left win!")
    else:
        print("ball inside")

    img_result = cv.bitwise_and(video_color, video_color, mask=img_mask)

    cv.imshow('img_result', img_result)

    if cv.waitKey(1) & 0xFF == 27:
        break

cv.destroyAllWindows()
