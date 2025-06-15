import pyttsx3
import sqlite3
from datetime import datetime
from speech_engine import speak_text

# Initialize the database connection
conn = sqlite3.connect("speech_data.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS speech_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        emotion TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# Initialize the speech engine
engine = pyttsx3.init()

# Set voice properties
engine.setProperty("rate", 150)  # Speed of speech
engine.setProperty("volume", 1.0)  # Volume level

# Get available voices and select one
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Change to 0 for male, 1 for female

# Intro speech - Benefits of Speech Synthesizer
intro_text = """
Hello! Welcome to the Speech Synthesizer project. 
This tool helps convert text into speech, making it useful for visually impaired individuals, 
language learning, audiobook creation, and hands-free applications. 
You can now enter your own text to hear it spoken aloud!
"""
engine.say(intro_text)
engine.runAndWait()

# Default speech statement
default_text = "Hello! Welcome to your speech synthesizer project."

# Emotion-based voice settings
emotions = {
    "happy": 180,  # Faster speech for happy tone
    "sad": 100,    # Slower speech for sad tone
    "excited": 200 # Very fast speech for excitement
}

# Ask the user to select an emotion
print("\nChoose an emotion: happy, sad, excited (or press Enter for normal)")
emotion = input("Enter emotion: ").strip().lower()

# Apply emotion-based settings if valid emotion is chosen
if emotion in emotions:
    engine.setProperty("rate", emotions[emotion])
    print(f"Emotion set to {emotion}. Adjusting speech rate.")

# Ask the user for input
user_text = input("\nEnter your statement (or press Enter to use default): ").strip()

# If the user enters nothing, use the default text
text_to_speak = user_text if user_text else default_text

# Store the user text in the database
cursor.execute("INSERT INTO speech_logs (text, emotion) VALUES (?, ?)", (text_to_speak, emotion))
conn.commit()

print("User text saved successfully!")

# Speak the text
engine.say(text_to_speak)
engine.runAndWait()

# Save the speech to an audio file
audio_filename = "speech_output.wav"
engine.save_to_file(text_to_speak, audio_filename)
engine.runAndWait()

print(f"Speech has been saved to {audio_filename}")

# Close database connection
conn.close()
