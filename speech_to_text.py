import tkinter as tk
import pyttsx3
import speech_recognition as sr
import threading
from playsound import playsound
import webbrowser
import os

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Create the main window
window = tk.Tk()
window.title("Real-time Speech-to-Text")

# Create a text widget to display recognized text
recognized_text = tk.Text(window, height=10, width=50)
recognized_text.pack()

# Create a label for notifications
notification_label = tk.Label(window, text="", fg="red")
notification_label.pack()

# Create a label for listening status
listening_status = tk.Label(window, text="Not Listening", fg="red")
listening_status.pack()

# Variable to keep track of listening state
listening = False

# Function to recognize speech and update UI in real-time
def recognize_speech():
    global listening
    while listening:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

            try:
                user_input = recognizer.recognize_google(audio)
                recognized_text.insert(tk.END,user_input + '\n' )
                recognized_text.see(tk.END)  # Scroll to the end
                print(f"You said: {user_input}")

                if user_input.lower() == "stop listening":
                    listening = False
                    stop_listening()
                if user_input.lower() == "anime girl":
                    listening = False
                    playsound('anime-girl.mp3')
            except sr.UnknownValueError:
                print("Can you please repeat...")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

# Function to start listening
def start_listening():
    global listening
    listening = True
    engine.say("I'm listening. Please start talking.")
    engine.runAndWait()
    listening_status.config(text="Listening", fg="green")
    threading.Thread(target=recognize_speech).start()

# Function to stop listening
def stop_listening():
    global listening
    listening = False
    listening_status.config(text="Stopped Listening", fg="red")
    engine.say("Stopped Listening.")
    engine.runAndWait()
    listening_status.pack_forget()  # Hide the label
    # show_notification("Stopped Listening")

# Function to exit the application
def exit_app():
    window.destroy()

# Function to show a notification
def show_notification(message):
    notification_label.config(text=message)

# Create a button to start listening
listen_button = tk.Button(window, text="Start Listening", command=start_listening)
listen_button.pack()

# Create a button to stop listening
stop_button = tk.Button(window, text="Stop Listening", command=stop_listening)
stop_button.pack()

# Create an exit button
exit_button = tk.Button(window, text="Exit", command=exit_app)
exit_button.pack()

window.mainloop()
