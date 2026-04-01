from tkinter import * 
from PIL import Image,ImageTk,ImageSequence 
import time
import pygame  
from pygame import mixer
mixer.init()

root = Tk()
root.geometry("1024x786")

def play_gif():
    root.lift()
    root.attributes("-topmost",True)
    global img
    img = Image.open("giphy.gif")
    lbl = Label(root)
    lbl.place(x=0,y=0)
    i=0
    mixer.music.load("start up.mp3")
    mixer.music.play()
    
    for img in ImageSequence.Iterator(img):
        img = img.resize((1024,786))
        img = ImageTk.PhotoImage(img)
        lbl.config(image=img)
        root.update()
        time.sleep(0.05)
    root.destroy()

play_gif()
root.mainloop()

import speech_recognition as sr
import threading
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QFont, QColor, QPainter, QPixmap
from PyQt6.QtCore import Qt, QTimer
import sys, subprocess, time

class JarvisOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Speech Recognition in Background
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = True  # Track listening status
        threading.Thread(target=self.listen_for_wake_word, daemon=True).start()  # Start background listening

    def initUI(self):
        self.setWindowTitle("JARVIS AI Overlay")
        self.showFullScreen()  
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.circle_size = 400
        self.circle_x = (self.width() - self.circle_size) // 2
        self.circle_y = (self.height() - self.circle_size) // 2

        # JARVIS Logo (Transparent)
        self.logo = QLabel(self)
        pixmap = QPixmap("jarvis-logo.png")
        pixmap = pixmap.scaled(self.circle_size, self.circle_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setGeometry(self.circle_x, self.circle_y, self.circle_size, self.circle_size)
        self.logo.setStyleSheet("background: transparent;")

        # Status Label
        self.status_label = QLabel("Listening...", self)
        self.status_label.setFont(QFont("Arial", 18))
        self.status_label.setStyleSheet("color: cyan; background: transparent;")
        self.status_label.setGeometry(self.width() // 2 - 100, self.height() // 2 + 250, 200, 50)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def listen_for_wake_word(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise

        while self.listening:
            with self.microphone as source:
                print("Listening for 'JARVIS'...")
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"You said: {command}")

                    if "jarvis" in command:
                        print("JARVIS Activated!")
                        self.status_label.setText("Activated!")
                        self.runJarvis()
                        time.sleep(3)  # Short pause before listening again
                        self.status_label.setText("Listening...")

                except sr.UnknownValueError:
                    pass  # Ignore if speech is not recognized
                except sr.RequestError:
                    print("Speech Recognition API unavailable")

    def runJarvis(self):
        subprocess.Popen(["python", "jarvis_main.py"])  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = JarvisOverlay()
    overlay.show()
    sys.exit(app.exec())

