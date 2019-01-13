import cv2
import numpy as np
from collections import deque
from matplotlib import pyplot as plt
import time

cap = cv2.VideoCapture(0)
hand_cascade = cv2.CascadeClassifier('OpenCV/haarcascades/hand.xml')

class Robot_Vision():
    def __init__(self, img):
        self.img = img

    def yellow_detection(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        Ymask = cv2.inRange(hsv, np.array([20, 65, 70]), np.array([30, 255, 255]))
        Y = cv2.bitwise_and(img, img, mask=Ymask)
        return Y

    def reconstruct(self, img):
        image = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
        img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        img_gray = cv2.Canny(img_gray, 100, 200)
        img_gray = np.float32(img_gray)
        dst = cv2.cornerHarris(img_gray, 2, 3, 0.04)

        coord = []
        coord = list(coord)
        image[dst > 0.01 * dst.max()] = [0, 0, 255]
        coord = np.where(np.all(image == (0, 0, 255), axis=-1))

        coor = list()
        sum1 = list()

        for i in zip(coord[0], coord[1]):
            a = list(i)
            coor.append(a)

        for i, j in coor:
            sum1.append(i + j)

        max_index = np.where(sum1 == max(sum1))[0]
        min_index = np.where(sum1 == min(sum1))[0]

        first = np.array(coor[int(min_index)])
        last = np.array(coor[int(max_index)])

        pts1 = np.float32([[first[0], first[1]], [first[0], last[1]], [last[0], first[1]], [last[0], last[1]]])
        pts2 = np.float32([[0, 0], [0, 300], [300, 0], [300, 300]])

        cv2.circle(image, (first[0], first[1]), 5, (255, 0, 0), -1)
        cv2.circle(image, (first[0], last[1]), 5, (0, 255, 0), -1)
        cv2.circle(image, (last[0], first[1]), 5, (0, 0, 255), -1)
        cv2.circle(image, (last[0], last[1]), 5, (0, 0, 0), -1)

        M = cv2.getPerspectiveTransform(pts1, pts2)

        dst = cv2.warpPerspective(img, M, (300, 300))

        return dst

    def find_diff(self, img, next_img):
        diff = cv2.absdiff(img, next_img)
        x = np.argmax(np.sum(diff, axis=0))
        y = np.argmax(np.sum(diff, axis=1))
        return x, y

    def moving_center(self, img, x, y):
        img_size = img.shape
        img_x = img_size[0]
        img_y = img_size[1]

        img_x = int(img_x / 2)
        img_y = int(img_y / 2)

        distance_x = img_x - x
        distance_y = img_y - y
    def hand_detection(self):

        frame = self.img
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hands = hand_cascade.detectMultiScale(gray, 1.1, 5)
        for (x, y, w, h) in hands:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


if __name__=='__main__':
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)
    print('start game')
    '''
    로봇팔 오목판으로 이동 후 캡쳐
    '''
    ret ,img = cap.read()
    img= cv2.imread('data/omok_1.PNG')
    img = cv2.resize(img, (500, 500))

    Vision = Robot_Vision(img)
    img_copy = np.copy(img)
    img = Vision.yellow_detection(img)
    img = Vision.reconstruct(img)

    '''
    서버에서 입력값대기 값 받으면 바둑알 옮기러 이동
    '''
    '''
    석션후 놓고 대기
    '''
    '''
    손 디텍션 후 차이 좌표 서버로 전송
    '''

    if detec:
        ret, next_img = cap.read()

    #img = dst[10:500, 10:500]

    cv2.imshow('origin', img_copy)
    cv2.imshow('prepro_img',img)

    cv2.waitKey(0)
    # if cv2.waitKey(1) == 27:
    #       break

