import cv2
import cvzone
from  cvzone.HandTrackingModule import HandDetector
import  random
import  time
# opening videocapture
cap = cv2.VideoCapture(0)

# width of window
cap.set(3, 640)

# height of window
cap.set(4, 480)

# only one hand can be detected
detector = HandDetector(maxHands=1)

# initial time
timer = 0

stateResult = False 
startGame = False

# initial score of computer and player
scores = [0, 0]

while True:
    imgKEVAL = cv2.imread("/Users/kevalpatel/Desktop/Keval/PROJECT/newproject/x.png")
    success, img = cap.read()
    imgScaled = cv2.resize(img, (0, 0), None, 0.78, 0.78)
    # slicing the height of window
    imgScaled = imgScaled[:, 96:404]

    # Find hands
    hands, img = detector.findHands(imgScaled)

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgKEVAL, str(int(timer)), (445, 271), cv2.FONT_HERSHEY_PLAIN, 6, (255, 255, 255), 4)

            if timer > 5:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    # stone 
                    if fingers == [0,0,0,0,0]:
                        playerMove = 1
                    # paper    
                    if fingers == [1,1,1,1,1]:
                        playerMove = 2
                    # scissor    
                    if fingers == [0,1,1,0,0]:
                        playerMove = 3
                    # generating random number from{1,2,3}
                    randomNumber = random.randint(1, 3)
                    # get the image 
                    imgAI = cv2.imread('/Users/kevalpatel/Desktop/Keval/PROJECT/newproject/'+str(randomNumber)+".png", cv2.IMREAD_UNCHANGED)
                    # print('/Users/kevalpatel/Desktop/Keval/PROJECT/newproject/',str(randomNumber)+".png")
                    imgKEVAL = cvzone.overlayPNG(imgKEVAL, imgAI, (23, 168))

                    # if player wins
                    if (playerMove == 1 and randomNumber == 3) or\
                        (playerMove == 2 and randomNumber == 1) or\
                        (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1
                        if scores[1]>=3 and scores[1]>scores[0]:
                            cv2.putText(imgKEVAL, str("COMPUTER WINS"), (415, 271), cv2.FONT_HERSHEY_PLAIN, 6, (255, 67, 255), 4)
                            scores[0] = 0
                            scores[1] = 0
                        

                    #  if COMPUTER Wins
                    if (playerMove == 3 and randomNumber == 1) or \
                        (playerMove == 1 and randomNumber == 2) or \
                        (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1
                        if scores[0]>=3 and scores[0]>scores[1]:
                            cv2.putText(imgKEVAL,str("PLAYER WIN"),(415, 271), cv2.FONT_HERSHEY_PLAIN, 6, (255, 67, 255), 4)
                            scores[0] = 0
                            scores[1] = 0
                    else:
                        pass 

    # load the window in right hand side box.
    imgKEVAL[166:540, 561:869] = imgScaled

    # load the stone,paper,scissoe images in left box.
    if stateResult:
        imgKEVAL = cvzone.overlayPNG(imgKEVAL, imgAI, (23, 168))

     # size,color and location of player and computer score
    cv2.putText(imgKEVAL, str(scores[0]), (391, 460), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgKEVAL, str(scores[1]), (500, 460), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    
    # title of game
    cv2.imshow("STONE PAPER SCISSOR GAME", imgKEVAL)

    key = cv2.waitKey(1)

    # starting the game if we press the key 's'
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False