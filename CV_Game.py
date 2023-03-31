import os
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone
import numpy as np
import time
import random
import cv2


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources/Game_Interface.png")



selection = -1
counter = 1
selectionSpeed = 7
detector = HandDetector(detectionCon=0.8, maxHands=1)
modePositions = [(1136, 196), (1000, 384), (1136, 581)]
counterPause = 0

# selectionList = [-1, -1, -1]

while True:
    success, img = cap.read()
    img=cv2.flip(img,1)
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw

    # overlaying the webcam feed on the background image
    imgBackground[139:139 + 480, 50:50 + 640] = img
    # imgBackground[0:720, 847: 1280] = listImgModes[modeType]

    # if hands and counterPause == 0 and modeType < 3:
    if hands and counterPause == 0:
        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)

        if fingers1 == [0, 1, 0, 0, 0]:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers1 == [0, 1, 1, 1, 0]:
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection = -1
            counter = 0

        if counter > 0:
            counter += 1
            print(counter)

            cv2.ellipse(imgBackground, modePositions[selection - 1], (103, 103), 0, 0, 
                    counter * selectionSpeed, (0, 255, 0), 20)

            if counter * selectionSpeed > 360:
            #     # selectionList[modeType] = selection
                # modeType += 1
                counter = 0
                # selection = -1
                counterPause = 1
                if selection ==1:
                    print("rock paper sissor")
                    cv2.destroyAllWindows()
                    rock_paper_sissor()
                elif selection ==2:
                    print("eat eatale things")
                    cv2.destroyAllWindows()
                    eatable_things()
                elif selection ==3:
                    print("ping pong")
                    cv2.destroyAllWindows()
                    pingpong()
                else:
                    selection = 0



    # To pause after each selection is made
    if counterPause > 0:
        counterPause += 1
        if counterPause > 60:
            counterPause = 0


    # Displaying
    # cv2.imshow("Image", img)
    cv2.imshow("Game_Interface", imgBackground)
    cv2.waitKey(1)

# ping pong game
    def pingpong():


        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)

        # Importing all images
        imgBackground = cv2.imread("Resources/Background.png")
        imgGameOver = cv2.imread("Resources/gameOver.png")
        imgBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)
        imgBat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
        imgBat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)

        # Hand Detector
        detector = HandDetector(detectionCon=0.8, maxHands=2)

        # Variables
        ballPos = [100, 100]
        speedX = 20
        speedY = 20
        gameOver = False
        score = [0, 0]

        while True:
            _, img = cap.read()
            img = cv2.flip(img, 1)
            imgRaw = img.copy()

            # Find the hand and its landmarks
            hands, img = detector.findHands(img, flipType=False)  # with draw

            # Overlaying the background image
            img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

            # Check for hands
            if hands:
                for hand in hands:
                    x, y, w, h = hand['bbox']
                    h1, w1, _ = imgBat1.shape
                    y1 = y - h1 // 2
                    y1 = np.clip(y1, 20, 415)

                    if hand['type'] == "Left":
                        img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                        if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                            speedX = -speedX
                            ballPos[0] += 30
                            score[0] += 1

                    if hand['type'] == "Right":
                        img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                        if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                            speedX = -speedX
                            ballPos[0] -= 30
                            score[1] += 1

            # Game Over
            if ballPos[0] < 40 or ballPos[0] > 1200:
                gameOver = True

            if gameOver:
                img = imgGameOver
                cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
                            2.5, (200, 0, 200), 5)

            # If game not over move the ball
            else:

                # Move the Ball
                if ballPos[1] >= 500 or ballPos[1] <= 10:
                    speedY = -speedY

                ballPos[0] += speedX
                ballPos[1] += speedY

                # Draw the ball
                img = cvzone.overlayPNG(img, imgBall, ballPos)

                cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
                cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

            img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))

            cv2.imshow("Image", img)
            key = cv2.waitKey(1)
            if key == ord('r'):
                ballPos = [100, 100]
                speedX = 20
                speedY = 20
                gameOver = False
                score = [0, 0]
                imgGameOver = cv2.imread("Resources/gameOver.png")

#rock paper sissor game 
    def rock_paper_sissor():

        cap =cv2.VideoCapture(0)
        # width
        cap.set(3, 648)
        # hight
        cap.set(4, 480)

        detector = HandDetector(maxHands=1)
        timer = 0
        stateResult = False
        startGame = False
        scores = [0, 0] # [AI, Player]

        while True:
            imgBG = cv2.imread("Resources/BG.png")
            success, img =cap.read()
            img=cv2.flip(img,1)

            imgScaled =cv2.resize(img,(0, 0), None, 0.875, 0.875)
            imgScaled = imgScaled[:,80:480]

            # find hands
            hands, img = detector.findHands(imgScaled)

            if startGame: 

                if stateResult  is False:
                    timer =time.time() - initialTime
                    cv2.putText(imgBG,str(int(timer)),(605,435),cv2.FONT_HERSHEY_PLAIN,6,(255,0,255),4)

                    if timer > 3:
                        stateResult = True
                        timer = 0

                        if hands:
                            playerMove = None
                            hand = hands[0]
                            fingers = detector.fingersUp(hand)
                            if fingers ==[0,0,0,0,0]:
                                playerMove = 1
                            if fingers ==[1,1,1,1,1]:
                                playerMove = 2
                            if fingers ==[0,1,1,0,0]:
                                playerMove = 3
                            if fingers ==[1,0,0,0,0]:
                                cv2.destroyAllWindows()
                                os.system("practice.py")

                            randomNumber = random.randint(1, 3)
                            imgAI = cv2.imread(f'Resources/{randomNumber}.png',cv2.IMREAD_UNCHANGED)
                            imgBG = cvzone.overlayPNG(imgBG,imgAI,(149,310))

                            # Player Wins
                            if (playerMove == 1 and randomNumber == 3) or \
                                    (playerMove == 2 and randomNumber == 1) or \
                                    (playerMove == 3 and randomNumber == 2):
                                scores[1] += 1

                            # AI Wins
                            if (playerMove == 3 and randomNumber == 1) or \
                                    (playerMove == 1 and randomNumber == 2) or \
                                    (playerMove == 2 and randomNumber == 3):
                                scores[0] += 1

                        # print(playerMove)

            imgBG[234:654,795:1195] = imgScaled

            if stateResult:
                imgBG = cvzone.overlayPNG(imgBG,imgAI,(149,310))


            cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
            cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

            # show camera video
            # cv2.imshow("Image", img)
            cv2.imshow("BG", imgBG)
            # cv2.imshow("Scaled", imgScaled)

            key = cv2.waitKey(1)
            if key == ord("s"):
                startGame = True
                initialTime = time.time()
                stateResult = False

# game eat eatable things
    def eatable_things():
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)

        detector = FaceMeshDetector(maxFaces=1)
        idList = [0, 17, 78, 292]

        # import images
        folderEatable = 'Objects/eatable'
        listEatable = os.listdir(folderEatable)
        eatables = []
        for object in listEatable:
            eatables.append(cv2.imread(f'{folderEatable}/{object}', cv2.IMREAD_UNCHANGED))

        folderNonEatable = 'Objects/noneatable'
        listNonEatable = os.listdir(folderNonEatable)
        nonEatables = []
        for object in listNonEatable:
            nonEatables.append(cv2.imread(f'{folderNonEatable}/{object}', cv2.IMREAD_UNCHANGED))

        currentObject = eatables[0]
        pos = [300, 0]
        speed = 5
        count = 0
        global isEatable
        isEatable = True
        gameOver = False


        def resetObject():
            global isEatable
            pos[0] = random.randint(100, 1180)
            pos[1] = 0
            randNo = random.randint(0, 2)  # change the ratio of eatables/ non-eatables
            if randNo == 0:
                currentObject = nonEatables[random.randint(0, 3)]
                isEatable = False
            else:
                currentObject = eatables[random.randint(0, 3)]
                isEatable = True

            return currentObject


        while True:
            success, img = cap.read()
            img=cv2.flip(img,1)

            if gameOver is False:
                img, faces = detector.findFaceMesh(img, draw=False)

                img = cvzone.overlayPNG(img, currentObject, pos)
                pos[1] += speed

                if pos[1] > 520:
                    currentObject = resetObject()

                if faces:
                    face = faces[0]
                    # for idNo,point in enumerate(face):
                    #     cv2.putText(img,str(idNo),point,cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),1)

                    up = face[idList[0]]
                    down = face[idList[1]]

                    for id in idList:
                        cv2.circle(img, face[id], 5, (255, 0, 255), 5)
                    cv2.line(img, up, down, (0, 255, 0), 3)
                    cv2.line(img, face[idList[2]], face[idList[3]], (0, 255, 0), 3)

                    upDown, _ = detector.findDistance(face[idList[0]], face[idList[1]])
                    leftRight, _ = detector.findDistance(face[idList[2]], face[idList[3]])

                    ## Distance of the Object
                    cx, cy = (up[0] + down[0]) // 2, (up[1] + down[1]) // 2
                    cv2.line(img, (cx, cy), (pos[0] + 50, pos[1] + 50), (0, 255, 0), 3)
                    distMouthObject, _ = detector.findDistance((cx, cy), (pos[0] + 50, pos[1] + 50))
                    print(distMouthObject)

                    # Lip opened or closed
                    ratio = int((upDown / leftRight) * 100)
                    # print(ratio)
                    if ratio > 60:
                        mouthStatus = "Open"
                    else:
                        mouthStatus = "Closed"
                    cv2.putText(img, mouthStatus, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)

                    if distMouthObject < 100 and ratio > 60:
                        if isEatable:
                            currentObject = resetObject()
                            count += 1
                        else:
                            gameOver = True
                cv2.putText(img, str(count), (1100, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 5)
            else:
                cv2.putText(img, "Game Over", (300, 400), cv2.FONT_HERSHEY_PLAIN, 7, (255, 0, 255), 10)

            cv2.imshow("Image", img)
            key = cv2.waitKey(1)

            if key == ord('r'):
                resetObject()
                gameOver = False
                count = 0
                currentObject = eatables[0]
                isEatable = True