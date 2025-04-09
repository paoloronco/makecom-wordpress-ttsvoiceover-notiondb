from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import texttospeech_v1
import uuid
import traceback

app = FastAPI()

# ✅ Configure your GCP bucket name and project ID here (DO NOT hardcode in production)
BUCKET_NAME = "your-bucket-name"
PROJECT_ID = "your-gcp-project-id"

# ✅ Request schema
class TTSRequest(BaseModel):
    text: str
    language: str = "it-IT"
    voice: str = "it-IT-Wavenet-B"
    filename: str | None = None

# ✅ Main endpoint
@app.post("/long-tts")
async def long_tts(req: TTSRequest):
    try:
        client = texttospeech_v1.TextToSpeechLongAudioSynthesizeClient()

        filename = req.filename or f"tts-{uuid.uuid4()}.wav"
        gcs_uri = f"gs://{BUCKET_NAME}/{filename}"

        # Set the TTS request parameters
        input_text = texttospeech_v1.SynthesisInput(text=req.text)
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code=req.language,
            name=req.voice
        )
        audio_config = texttospeech_v1.AudioConfig(
            audio_encoding=texttospeech_v1.AudioEncoding.LINEAR16
        )

        # Call the GCP TTS API
        operation = client.synthesize_long_audio(
            request={
                "parent": f"projects/{PROJECT_ID}/locations/europe-west12",
                "input": input_text,
                "voice": voice,
                "audio_config": audio_config,
                "output_gcs_uri": gcs_uri
            }
        )

        return {
            "status": "started",
            "gcs_uri": gcs_uri,
            "filename": filename,
            "operation": operation.operation.name
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        traceback.print_exc()
        return {"error": str(e)}

# ✅ Required for Cloud Run: listen on port 8080
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
