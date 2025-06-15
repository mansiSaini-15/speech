import customtkinter as ctk
import tkinter as tk
import speech_engine
import database
import pyttsx3
from database import save_speech_log

# Initialize GUI Window
ctk.set_appearance_mode("light")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  

app = ctk.CTk()  
app.geometry("600x400")
app.title("Speech Synthesizer")

# Text Input Box
text_label = ctk.CTkLabel(app, text="Enter Text:")
text_label.pack(pady=5)
text_entry = ctk.CTkEntry(app, width=400)
text_entry.pack(pady=5)

# Emotion Selection Dropdown
emotion_label = ctk.CTkLabel(app, text="Select Emotion:")
emotion_label.pack(pady=5)
emotion_var = tk.StringVar(value="Neutral")
emotion_dropdown = ctk.CTkComboBox(app, values=["Neutral", "Happy", "Sad", "Angry", "Calm"], variable=emotion_var)
emotion_dropdown.pack(pady=5)

# Function to Generate Speech
def generate_speech():
    text = text_entry.get()
    emotion = emotion_var.get()
    print(f"Text: {text}, Emotion: {emotion}")

    if text:
        save_speech_log(text, emotion)  # Save to Database
        text_to_speech(text, emotion)

import pyttsx3

def text_to_speech(text, emotion):
    engine = pyttsx3.init()

    # Debug: Check available voices
    voices = engine.getProperty("voices")
    print("Available Voices:", voices)  

    if emotion == "Happy":
        engine.setProperty("rate", 180)
    elif emotion == "Sad":
        engine.setProperty("rate", 120)
    elif emotion == "Angry":
        engine.setProperty("rate", 200)
    elif emotion == "Calm":
        engine.setProperty("rate", 140)
    else:
        engine.setProperty("rate", 150)  # Default speed

    print(f"Speaking: {text} with emotion: {emotion}")  # Debugging print
    engine.say(text)
    engine.runAndWait()



# Button to Convert Text to Speech
speak_button = ctk.CTkButton(app, text="Speak", command=generate_speech)
speak_button.pack(pady=10)

# Exit Button
exit_button = ctk.CTkButton(app, text="Exit", command=app.quit)
exit_button.pack(pady=5)

app.mainloop()
