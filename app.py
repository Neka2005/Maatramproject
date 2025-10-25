from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import speech_recognition as sr

app = FastAPI()

# -------- CORS Setup --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Load Sentiment Analysis Model --------
sentiment_model = pipeline("sentiment-analysis")

# -------- Helper Function: Voice to Text --------
def voice_to_text(file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

# -------- Text Input --------
class TextInput(BaseModel):
    text: str

@app.post("/analyze-text")
def analyze_text(input: TextInput):
    result = sentiment_model(input.text)[0]
    sentiment = result['label']
    confidence = round(result['score'] * 100, 2)
    status = "✅ Approved" if sentiment == "POSITIVE" else ("⚠ Review" if sentiment == "NEUTRAL" else "❌ Not Suitable")
    return {
        "text": input.text,
        "sentiment": sentiment,
        "confidence": f"{confidence}%",
        "verification_status": status
    }

# -------- Voice Input --------
@app.post("/analyze-voice")
async def analyze_voice(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = voice_to_text(file_path)
    if not text:
        return {"error": "Could not understand audio"}

    result = sentiment_model(text)[0]
    sentiment = result['label']
    confidence = round(result['score'] * 100, 2)
    status = "✅ Approved" if sentiment == "POSITIVE" else ("⚠ Review" if sentiment == "NEUTRAL" else "❌ Not Suitable")
    return {
        "text": text,
        "sentiment": sentiment,
        "confidence": f"{confidence}%",
        "verification_status": status
    }