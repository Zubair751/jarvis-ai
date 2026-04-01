import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import threading
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pyautogui
import os

# Initialize speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

# Function to make AI speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to take voice commands
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)
    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}")
        return query.lower()
    except Exception as e:
        print("Say that again")
        return ""

# Function to handle commands
def handle_command(query):
    if "wake up" in query:
        greetMe()
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {current_time}")
    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak(f"According to Wikipedia: {results}")
    elif "open" in query:
        app = query.replace("open", "").strip()
        speak(f"Opening {app}")
        pyautogui.press("super")
        pyautogui.typewrite(app)
        pyautogui.sleep(2)
        pyautogui.press("enter")
    elif "exit" in query or "stop" in query:
        speak("Goodbye!")
        root.destroy()
    else:
        speak("I'm sorry, I don't understand that command.")

# Function to greet the user
def greetMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning, sir")
    elif 12 <= hour < 18:
        speak("Good Afternoon, sir")
    else:
        speak("Good Evening, sir")
    speak("Please tell me, How can I help you?")

# Function to start listening
def start_listening():
    while True:
        query = take_command()
        if query:
            handle_command(query)

# Transparent Overlay GUI with GIF
def create_overlay():
    overlay = tk.Tk()
    overlay.attributes("-fullscreen", True)
    overlay.attributes("-topmost", True)
    overlay.attributes("-transparentcolor", "white")
    overlay.configure(bg="white")

    # Load GIF
    gif_path = "giphy.gif"  # Replace with your GIF path
    gif = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(gif)]

    # Display GIF
    label = tk.Label(overlay, bg="white")
    label.pack()

    # Function to update GIF frames
    def update_gif(frame):
        frame = (frame + 1) % len(frames)
        label.config(image=frames[frame])
        overlay.after(100, update_gif, frame)

    # Start GIF animation
    overlay.after(0, update_gif, 0)

    # Click event to activate J.A.R.V.I.S.
    def activate_jarvis(event):
        overlay.destroy()
        threading.Thread(target=start_listening).start()

    label.bind("<Button-1>", activate_jarvis)
    overlay.mainloop()

# Run the overlay
create_overlay()