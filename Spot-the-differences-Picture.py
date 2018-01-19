# -*- coding: UTF-8 -*-

import time
from PIL import ImageGrab
from PIL import ImageChops
import cv2
import numpy as np
import win32gui
import win32api
import win32con
per_time = 2
wd_name = "大家来找茬"
wd_class_name = "#32770"
hwnd=win32gui.FindWindow(wd_class_name,wd_name)
base_width=1024
base_height=768
print(hwnd)
if hwnd == 0:
    print("not found")   
else:
    win32gui.SetForegroundWindow(hwnd)
    game_rect = win32gui.GetWindowRect(hwnd)
    time.sleep(3)
    print(game_rect[0],game_rect[1],game_rect[2],game_rect[3])
    width = game_rect[2] - game_rect[0]
    height = game_rect[3] - game_rect[1]
    rate_width=width/base_width
    rate_height=height/base_height
    rect1 = (game_rect[0]+int(92*rate_width),game_rect[1]+int(312*rate_height),game_rect[0]+width/2-int(37*rate_width),game_rect[1]++int(598*rate_height))   #沿中线分开，+55是因为去掉图像的左边沿
    rect2 = (game_rect[0]+width/2+int(37*rate_width),game_rect[1]++int(312*rate_height),game_rect[2]-int(92*rate_width),game_rect[1]++int(598*rate_height))   #沿中线分开，-55是因为去掉图像的右边沿
    ima = ImageGrab.grab(rect1)
    imb = ImageGrab.grab(rect2)
    out = ImageChops.difference(ima,imb)   #比较两幅图
    ima.save("test1.jpg",'jpeg')
    imb.save("test2.jpg",'jpeg')
    out.save("out.jpg",'jpeg')


    img1 = cv2.imread("out.jpg")
    img1 = cv2.medianBlur(img1,3)

    hsv=cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)

    
    ##lower=np.array([25,25,25], dtype=np.uint8)
    ##upper=np.array([255,255,255], dtype=np.uint8)
    ##mask=cv2.inRange(img1,lower,upper)
    lower_blue=np.array([0,0,0], dtype=np.uint8)
    upper_blue=np.array([255,255,30], dtype=np.uint8)
    mask=cv2.inRange(hsv,lower_blue,upper_blue)
    # 根据阈值构建掩模
    kernel = np.ones((1,1),np.uint8)
    mask_img,contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)   
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    list_cnt=[]
    for cnt in contours:
        area = cv2.contourArea(cnt)
        list_cnt.append({"area":area,"cnt":cnt})
    list_cnt.sort(key=lambda obj:obj.get('area'), reverse=True)
    index=0
    for i in range(len(list_cnt)):
        x,y,w,h = cv2.boundingRect(list_cnt[i]['cnt'])
        if i < 5:
            dst = cv2.rectangle(img1,(x,y),(x+w,y+h),(255,0,0),2)
            pos = [int(rect1[0]+x+w/2),int(rect1[1]+y+h/2)]
            win32api.SetCursorPos(pos)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        else:
           dst = cv2.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),2)
           
        time.sleep(per_time)

        
    test1 = cv2.imread("test1.jpg")
    test2 = cv2.imread("test2.jpg")
    cv2.imshow('test1.jpg',test1)
    cv2.imshow('test2.jpg',test2)
    cv2.imshow('img1',img1)
    cv2.imshow('img',mask)
    cv2.imshow('dst',dst)

