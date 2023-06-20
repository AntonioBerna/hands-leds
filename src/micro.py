import serial.tools.list_ports
import pyfirmata
import platform
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

    def __init__(self, port: str) -> None:
        board = pyfirmata.Arduino(port)
        self.leds = []
        for i in range(0, self.hands):
            self.leds.append(board.get_pin(f"d:{i + self.start_pin}:o"))

    def write_text(self, frame, finger_count: int) -> None:
        cv2.putText(frame, f"Finger count: {finger_count}",
                        org=(20, 30),
                        fontFace=cv2.FONT_HERSHEY_COMPLEX,
                        fontScale=1,
                        color=(255, 255, 255),
                        thickness=1,
                        lineType=cv2.LINE_AA)

    def set_leds(self, frame, fingers: list) -> None:
        match fingers:
            case self.ZERO_FINGER:
                for i in range(0, self.hands):
                    self.leds[i].write(0)
                self.write_text(frame, sum(self.ZERO_FINGER))
            case self.ONE_FINGER:
                self.leds[0].write(1)
                for i in range(1, self.hands):
                    self.leds[i].write(0)
                self.write_text(frame, sum(self.ONE_FINGER))
            case self.TWO_FINGER:
                for i in range(0, 2):
                    self.leds[i].write(1)
                for i in range(2, self.hands):
                    self.leds[i].write(0)
                self.write_text(frame, sum(self.TWO_FINGER))
            case self.THREE_FINGER:
                for i in range(0, 3):
                    self.leds[i].write(1)
                for i in range(3, self.hands):
                    self.leds[i].write(0)
                self.write_text(frame, sum(self.THREE_FINGER))
            case self.FOUR_FINGER:
                for i in range(0, 4):
                    self.leds[i].write(1)
                self.leds[self.hands - 1].write(0)
                self.write_text(frame, sum(self.FOUR_FINGER))
            case self.FIVE_FINGER:
                for i in range(0, self.hands):
                    self.leds[i].write(1)
                self.write_text(frame, sum(self.FIVE_FINGER))


def get_arduino_serial_ports() -> list:
    ports = serial.tools.list_ports.comports()
    arduino_ports = []
    
    if platform.system() == "Darwin":
        for port in ports:
            if "usbmodem" in port.device or "usbserial" in port.device:
                arduino_ports.append(port.device)
    elif platform.system() == "Linux":
        for port in ports:
            if "ttyUSB" in port.device or "ttyACM" in port.device:
                arduino_ports.append(port.device)
    
    return arduino_ports
