import cv2 as cv
import numpy as np
import module as m
import time
import datetime



camera = cv.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
f = camera.get(cv.CAP_PROP_FPS)
width = camera.get(cv.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv.CAP_PROP_FRAME_HEIGHT)


def eyePos(frame):
    COUNTER = 0
    TOTAL_BLINKS = 0
    CLOSED_EYES_FRAME = 3
    cameraID = 0
    videoPath = "Video/Your Eyes Independently_Trim5.mp4"
    # variables for frame rate.
    FRAME_COUNTER = 0
    START_TIME = time.time()
    FPS = 0
    FRAME_COUNTER += 1
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    height, width = grayFrame.shape
    circleCenter = (int(width/2), 50)
    pos=""
    leftPos=""
    # calling the face detector funciton
    image, face,no_person = m.faceDetector(frame, grayFrame)
    if face is not None:

        # calling landmarks detector funciton.
        image, PointList = m.faceLandmakDetector(frame, grayFrame, face, False)
        # print(PointList)

        #cv.putText(frame, f'FPS: {round(FPS,1)}',(460, 20), m.fonts, 0.7, m.YELLOW, 2)
        RightEyePoint = PointList[36:42]
        LeftEyePoint = PointList[42:48]
        leftRatio, topMid, bottomMid = m.blinkDetector(LeftEyePoint)
        rightRatio, rTop, rBottom = m.blinkDetector(RightEyePoint)
        # cv.circle(image, topMid, 2, m.YELLOW, -1)
        # cv.circle(image, bottomMid, 2, m.YELLOW, -1)

        blinkRatio = (leftRatio + rightRatio)/2
        #cv.circle(image, circleCenter, (int(blinkRatio*4.3)), m.CHOCOLATE, -1)
        #cv.circle(image, circleCenter, (int(blinkRatio*3.2)), m.CYAN, 2)
        #cv.circle(image, circleCenter, (int(blinkRatio*2)), m.GREEN, 3)

        if blinkRatio > 4:
            COUNTER += 1
            #cv.putText(image, f'Blink', (70, 50),m.fonts, 0.8, m.LIGHT_BLUE, 2)
            # print("blink")
        else:
            if COUNTER > CLOSED_EYES_FRAME:
                TOTAL_BLINKS += 1
                COUNTER = 0
        #cv.putText(image, f'Total Blinks: {TOTAL_BLINKS}', (230, 17),m.fonts, 0.5, m.ORANGE, 2)

        # for p in LeftEyePoint:
        #     cv.circle(image, p, 3, m.MAGENTA, 1)
        mask, pos, color = m.EyeTracking(frame, grayFrame, RightEyePoint)
        maskleft, leftPos, leftColor = m.EyeTracking(
            frame, grayFrame, LeftEyePoint)
        text_right=pos
        text_left=leftPos
        #cv.line(image, (30, 90), (100, 90), color[0], 30)
        #cv.line(image, (25, 50), (135, 50), m.WHITE, 30)
        #cv.line(image, (int(width-150), 50), (int(width-45), 50), m.WHITE, 30)
        #cv.line(image, (int(width-140), 90),(int(width-60), 90), leftColor[0], 30)

        # writing text on above line
        #cv.putText(image, f'{pos}', (35, 95), m.fonts, 0.6, color[1], 2)
        #cv.putText(image, f'{leftPos}', (int(width-140), 95),m.fonts, 0.6, leftColor[1], 2)
        #cv.putText(image, f'Right Eye', (35, 55), m.fonts, 0.6, color[1], 2)
        #cv.putText(image, f'Left Eye', (int(width-145), 55), m.fonts, 0.6, leftColor[1], 2)
    return image,pos,leftPos,no_person