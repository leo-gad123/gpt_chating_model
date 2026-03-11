# voice_response_debug_gemini.py

import speech_recognition as sr
import pyttsx3
from google import genai

# ----------------------------
# 1️⃣ Initialize Google Gemini Client
# ----------------------------
API_KEY = "AIzaSyAsbUxL1KL9b5FCPG4nQd0uI40VYRos8uc"  # replace with your actual API key
client = genai.Client(api_key=API_KEY)
chat = client.chats.create(model="gemini-2.5-flash")

# ----------------------------
# 2️⃣ Initialize Speech Recognizer
# ----------------------------
recognizer = sr.Recognizer()
mic = sr.Microphone()

# ----------------------------
# 3️⃣ Initialize pyttsx3 TTS engine
# ----------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)   # speech rate
engine.setProperty('volume', 1.0) # volume (0.0 to 1.0)

print("Voice assistant ready. Say 'quit' to exit.\n")

while True:
    # ----------------------------
    # Listen to user voice
    # ----------------------------
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        audio = recognizer.listen(source)

    # ----------------------------
    # Convert voice to text
    # ----------------------------
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"[DEBUG] Recognized text: {user_input}")
    except sr.UnknownValueError:
        print("[DEBUG] Could not understand audio")
        engine.say("Sorry, I could not understand you.")
        engine.runAndWait()
        continue
    except sr.RequestError as e:
        print(f"[DEBUG] STT request error: {e}")
        engine.say("There was an error with speech recognition.")
        engine.runAndWait()
        continue

    # Exit condition
    if user_input.strip().lower() in ["quit", "exit", "stop"]:
        print("[DEBUG] Exiting voice assistant...")
        engine.say("Goodbye!")
        engine.runAndWait()
        break

    # ----------------------------
    # Send text to Gemini chat
    # ----------------------------
    try:
        response = chat.send_message(user_input)
        ai_reply = response.text
        print(f"[DEBUG] AI response text: {ai_reply}")
    except Exception as e:
        print(f"[DEBUG] Error sending message to Gemini: {e}")
        engine.say("There was an error connecting to the AI.")
        engine.runAndWait()
        continue

    # ----------------------------
    # Speak the AI reply out loud
    # ----------------------------
    try:
        engine.say(ai_reply)
        engine.runAndWait()
        print("[DEBUG] AI response spoken successfully")
    except Exception as e:
        print(f"[DEBUG] TTS error: {e}")