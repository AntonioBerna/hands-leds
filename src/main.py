from cvzone.HandTrackingModule import HandDetector
import tkinter as tk
from tkinter import StringVar, messagebox
import sys

from micro import MicroController, get_arduino_serial_ports, cv2

class HandsLedsApp(MicroController):
    def __init__(self, ports: list) -> None:
        self.window = tk.Tk()
        self.window.title("Hands & Leds")
        self.window.geometry("245x95")
        self.window.resizable(False, False)
        
        self.selected_port_var = StringVar(self.window)
        self.selected_port_var.set("Select port")

        self.port_menu = tk.OptionMenu(self.window, self.selected_port_var, *ports)
        self.port_menu.pack(padx=10, pady=10)

        self.button = tk.Button(self.window, text="Open Camera", command=self.on_start)
        self.button.pack(pady=10)

    def on_start(self) -> None:
        selected_port = self.selected_port_var.get()
        if selected_port == "Select port":
            messagebox.showwarning("Warning", "Please select a port.")
            return
        
        super().__init__(port=selected_port)
        video = cv2.VideoCapture(0)
        detector = HandDetector(detectionCon=0.8, maxHands=1)

        while True:
            _, frame = video.read()
            # frame = cv2.flip(frame, 1)

            hands, _ = detector.findHands(frame)
            if hands:
                fingers = detector.fingersUp(hands[0])
                self.set_leds(frame=frame, fingers=fingers)
            else:
                self.set_leds(frame=frame, fingers=[0 for _ in range(5)])

            cv2.imshow("Hands & Leds", frame)

            if cv2.waitKey(1) == ord("q"):
                break
        
        video.release()
        cv2.destroyAllWindows()

    def run(self) -> None:
        self.window.mainloop()


if __name__ == "__main__":
    ports = get_arduino_serial_ports()
    if not ports:
        print("No Arduino port found.")
        sys.exit()

    app = HandsLedsApp(ports)
    app.run()
