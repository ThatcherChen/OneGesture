import cv2
import applescript
import numpy as np
import time

from handUtil import HandDetector

# 打开摄像头
cap = cv2.VideoCapture(0)
# 创建一个手势识别对象
detector = HandDetector()

# 指尖列表，分别代表大拇指、食指、中指、无名指和小指的指尖
tip_ids = [4, 8, 12, 16, 20]
dx, dy = 0, 0
num = 0
volume = 0
ifOn = False
applescript.run('set volume output volume ' + str(volume))
while True:
    success, img = cap.read()

    if success:
        # 检测手势
        img = detector.find_hands(img, draw=True)
        # 获取手势数据
        lmslist = detector.find_positions(img)
        if len(lmslist) > 0:
            fingersX = []
            fingersY = []
            for tid in tip_ids:
                # 找到每个指尖的位置
                x, y = lmslist[tid][1], lmslist[tid][2]
                cv2.circle(img, (x, y), 8, (255, 255, 0), cv2.FILLED)
                # 记录大拇指的位置
                if tid == 4:
                    fingersX.append(x)
                    fingersY.append(y)
                # 记录食指的位置
                if tid == 8:
                    fingersX.append(x)
                    fingersY.append(y)
            dx = fingersX[0] - fingersX[1]
            dy = fingersY[0] - fingersY[1]

            cv2.line(img, (fingersX[0], fingersY[0]), (fingersX[1], fingersY[1]), (0, 0, 255), 4, 8)

        cv2.imshow('Image', img)

        # 使用AppleScript控制电脑，在Windows下也可以使用其它脚本控制
        if dy > 100:
            ifOn = False
        else:
            ifOn = True
        if ifOn:
            volume = int(dx + 50)
            if volume > 100:
                volume = 100
            if volume < 0:
                volume = 0
            applescript.run('set volume output volume ' + str(volume))

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
