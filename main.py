from cvzone.HandTrackingModule import HandDetector
import pyfirmata
import cv2

class MicroController:
    hands = 5
    start_pin = 8
    
    ZERO_FINGER = [0 for _ in range(hands)]
    ONE_FINGER = [0, 1, 0, 0, 0]
    TWO_FINGER = [0, 1, 1, 0, 0]
    THREE_FINGER = [0, 1, 1, 1, 0]
    FOUR_FINGER = [0, 1, 1, 1, 1]
    FIVE_FINGER = [1, 1, 1, 1, 1]

    def __init__(self, port):
        board = pyfirmata.Arduino(port)
        self.leds = []
        for i in range(0, self.hands):
            self.leds.append(board.get_pin(f"d:{i + 8}:o"))

    def write_text(self, frame, finger_count):
        cv2.putText(frame, f"Finger count: {finger_count}",
                        org=(20, 460),
                        fontFace=cv2.FONT_HERSHEY_COMPLEX,
                        fontScale=1,
                        color=(255, 255, 255),
                        thickness=1,
                        lineType=cv2.LINE_AA)

    def set_leds(self, frame, fingers):
        if fingers == self.ZERO_FINGER:
            for i in range(0, self.hands):
                self.leds[i].write(0)
            self.write_text(frame, sum(self.ZERO_FINGER))
        elif fingers == self.ONE_FINGER:
            self.leds[0].write(1)
            for i in range(1, self.hands):
                self.leds[i].write(0)
            self.write_text(frame, sum(self.ONE_FINGER))
        elif fingers == self.TWO_FINGER:
            for i in range(0, 2):
                self.leds[i].write(1)
            for i in range(2, self.hands):
                self.leds[i].write(0)
            self.write_text(frame, sum(self.TWO_FINGER))
        elif fingers == self.THREE_FINGER:
            for i in range(0, 3):
                self.leds[i].write(1)
            for i in range(3, self.hands):
                self.leds[i].write(0)
            self.write_text(frame, sum(self.THREE_FINGER))
        elif fingers == self.FOUR_FINGER:
            for i in range(0, 4):
                self.leds[i].write(1)
            self.leds[self.hands - 1].write(0)
            self.write_text(frame, sum(self.FOUR_FINGER))
        elif fingers == self.FIVE_FINGER:
            for i in range(0, self.hands):
                self.leds[i].write(1)
            self.write_text(frame, sum(self.FIVE_FINGER))

def main():
    video = cv2.VideoCapture(0)
    # video.set(3, 640) # width, pixel
    # video.set(4, 480) # height, pixel
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    mc = MicroController(port="/dev/cu.usbmodem14201")

    while True:
        _, frame = video.read()
        # frame = cv2.flip(frame, 1)

        hands, _ = detector.findHands(frame)
        if hands:
            fingers = detector.fingersUp(hands[0])
            mc.set_leds(frame=frame, fingers=fingers)
        
        cv2.imshow("Hands and Leds", frame)
        
        if cv2.waitKey(1) == ord("q"):
            break
    
    mc.set_leds(frame=frame, fingers=[0 for _ in range(5)])
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
