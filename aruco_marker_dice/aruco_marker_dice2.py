# aruco marker 주사위

import numpy as np
import cv2
import cv2.aruco as aruco
import winsound
from roboid import *

def sound(i):
    sol = {'do': 261, 're': 293, 'mi': 329, 'pa': 349, 'sol': 391, 'ra': 440, 'si': 493}
    mel = ['do', 'mi', 'mi', 'mi', 'sol', 'sol', 're', 'pa', 'pa']
    dur = [4, 4, 2, 4, 4, 2, 4, 4, 2]
    mel2 = ['si', 're']
    dur2 = [1, 1]
    music = zip(mel, dur)
    music2 = zip(mel2, dur2)

    if i == 1:
        for melody, duration in music2:
            winsound.Beep(sol[melody], 100 // duration)
    elif i == 2:
        for melody, duration in music:
            winsound.Beep(sol[melody], 1000 // duration)

# 노트북 웹캠이 있다면 VideoCapture의 인자를 1로, 없다면 0으로.
cam = cv2.VideoCapture(1)
dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
hamster0 = HamsterS(0)
hamster1 = HamsterS(1)
counter = 0
wait_time = 30
occupation = 0
hamster_speed = 80

# hamster 0 first. turn == 1 -> hamster 0 , turn == -1 -> hamster 1
turn = 1

def handle_movement(number):
    winsound.Beep(100 + 300 * number, 50)

    proximity_check = 0
    loop_limit = number * 25 + 25
    loop = 0

    if turn == -1:
        while loop < loop_limit:
            hamster0.wheels(hamster_speed)
            wait(20)
            loop += 1
            if hamster0.left_proximity() > 60 or hamster0.right_proximity() > 60 :
                proximity_check = 1
                wait(20)
                break
    elif turn == 1:
        while loop < loop_limit:
            hamster1.wheels(hamster_speed)
            wait(20)
            loop += 1
            if hamster1.left_proximity() > 60 or hamster1.right_proximity() > 60 :
                proximity_check = 1
                wait(20)
                break

    hamster0.stop()
    hamster1.stop()

    wait(40)

    return proximity_check

def hamster_ceremony():
    if turn == -1:
        hamster0.note(52, 0.5)
        hamster0.note(56, 0.5)
        hamster0.note(59, 0.5)
        hamster0.note(64, 1)
        hamster0.wheels(100,-100)
        wait(2000)
    elif turn == 1:
        hamster1.note(52, 0.5)
        hamster1.note(56, 0.5)
        hamster1.note(59, 0.5)
        hamster1.note(64, 1)
        hamster1.wheels(100, -100)
        wait(2000)

while True:

    _, image = cam.read()
    image = image[35:595, 110:540]
    image = cv2.rectangle(image, (105,115), (325, 325), (255,0,0), 1, cv2.LINE_8)
    corners, ids, rejected = aruco.detectMarkers(image, dictionary)
    counter += 1
    wait(100)
    num_image = np.zeros((320, 320, 3), np.uint8)
    cv2.imshow('num_image', num_image)
    cv2.imshow('image', image)

    if ids is None:
        occupation = 0
    if counter > wait_time and occupation == 0 and ids is not None:
        aruco.drawDetectedMarkers(image, corners, borderColor=(0, 0, 255))
        ids_para = ids[0,0]
        if ids_para == 0:
            cv2.putText(num_image, "1", (60, 250), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 8, cv2.LINE_AA)
        elif ids_para == 1:
            cv2.putText(num_image, "2", (60, 250), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 8, cv2.LINE_AA)
        elif ids_para == 2:
            cv2.putText(num_image, "3", (60, 250), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 8, cv2.LINE_AA)
        elif ids_para == 3:
            cv2.putText(num_image, "4", (60, 250), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 8, cv2.LINE_AA)
        elif ids_para == 4:
            cv2.putText(num_image, "5", (60, 250), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 8, cv2.LINE_AA)
        elif ids_para == 5:
            cv2.putText(num_image, "6", (60, 250), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 8, cv2.LINE_AA)
        game_over = handle_movement(ids_para)
        if game_over == 1:
            hamster0.stop()
            hamster1.stop()
            wait(20)
            print("game over!")
            hamster_ceremony()
            break
        turn *= -1
        occupation = 1
        counter = 0
        cv2.imshow('num_image', num_image)
        cv2.imshow('image', image)
        sound(2)

    if counter > wait_time + 30 or occupation == 1:
        empty_image = np.full((320, 320, 3), (0, 0, 0), np.uint8)
        cv2.putText(empty_image, "Roll the Dice", (60, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow('image', empty_image)
        cv2.waitKey(100)
        sound(1)
        wait(1000)
        counter = 0
        continue
    if cv2.waitKey(1) == 27:
        break