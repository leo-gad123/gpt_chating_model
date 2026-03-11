from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from google import genai
import speech_recognition as sr
import pyttsx3

app = FastAPI()
client = genai.Client(api_key="AIzaSyAsbUxL1KL9b5FCPG4nQd0uI40VYRos8uc")

# Text request schema
class ChatRequest(BaseModel):
    message: str

# Text-based chat
@app.post("/chat/")
async def chat_text(request: ChatRequest):
    try:
        chat = client.chats.create(model="gemini-2.5-flash")
        response = chat.send_message(request.message)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}

# Voice-based chat
@app.post("/chat-voice/")
async def chat_voice(file: UploadFile = File(...)):
    try:
        # Save uploaded audio file temporarily
        audio_path = f"temp_{file.filename}"
        with open(audio_path, "wb") as f:
            f.write(await file.read())
        
        # Recognize speech from audio
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        # Send recognized text to GenAI
        chat = client.chats.create(model="gemini-2.5-flash")
        response = chat.send_message(text)
        ai_text = response.text

        # Convert AI text to speech
        engine = pyttsx3.init()
        audio_output = f"response_{file.filename}.mp3"
        engine.save_to_file(ai_text, audio_output)
        engine.runAndWait()

        return {"recognized_text": text, "ai_response_text": ai_text, "audio_file": audio_output}

    except Exception as e:
        return {"error": str(e)}