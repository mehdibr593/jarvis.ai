import os
import platform
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
from dotenv import load_dotenv

# Load key from the hidden .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    print("Error: No API Key found. Please check your .env file.")
    exit()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

engine = pyttsx3.init()
if platform.system() == "Windows":
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
else:
    engine.setProperty("rate", 160)

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_for_wake_word():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    with sr.Microphone() as source:
        print(f"--- Jarvis AI Active ({platform.system()}) ---")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while True:
            try:
                audio = recognizer.listen(source, phrase_time_limit=5)
                query = recognizer.recognize_google(audio).lower()
                if "jarvis" in query:
                    speak("System online. How can I help you?")
                    audio_cmd = recognizer.listen(source)
                    command = recognizer.recognize_google(audio_cmd)
                    response = model.generate_content(command)
                    speak(response.text)
            except Exception:
                continue

if __name__ == "__main__":
    listen_for_wake_word()
