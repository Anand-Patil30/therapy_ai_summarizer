from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import shutil
import uuid
import json
import traceback
import logging

from my_project.audio_processing import convert_audio, stt_transcribe, diarize_audio, merge_results
from my_project.crew import TherapySummarizer

# Paths for uploads and output
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.normpath(os.path.join(THIS_DIR, "..", "audio_samples"))
OUTPUT_DIR = os.path.normpath(os.path.join(THIS_DIR, "..", "output"))

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()

def format_merged_transcript(merged_path):
    """
    Returns speaker-tagged transcript string for LLM summarization.
    """
    with open(merged_path, 'r') as f:
        segments = json.load(f)
    lines = [f"{seg.get('speaker', 'unknown')}: {seg.get('text', '')}" for seg in segments]
    return "\n".join(lines)

@app.post("/analyze_audio/")
async def analyze_audio(file: UploadFile = File(...)):
    # Save the uploaded audio file
    unique_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1] or ".wav"
    audio_path = os.path.join(UPLOAD_DIR, f"{unique_id}{ext}")

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1. Convert audio
        wav_path = convert_audio.convert_audio(audio_path)
        print("Converted", wav_path)
        # 2. Transcribe
        transcript_path = stt_transcribe.transcribe(wav_path)
        print("Transcripted", transcript_path)
        # 3. Diarization
        diarization_path = diarize_audio.diarize(wav_path)
        print("Diarized", diarization_path)
        # 4. Merge
        merged_json_path = merge_results.merge()

        # 5. Prepare transcript for CrewAI summarizer
        transcript_str = format_merged_transcript(merged_json_path)
        crew = TherapySummarizer()
        result = crew.kickoff(inputs={"transcript_text": transcript_str})
        print("result type",type(result))
        print("\n\n\n*******. Result ******\n\n\n", "\n" + str(result) + "\n")
        with open(merged_json_path, 'r') as f:
            merged_data = json.load(f)

        logging.info(f"Full crew kickoff result: {result}")
        if isinstance(result, str):
            summary_text = result
        else:
            # Try to get the full text from result.raw if available
            if hasattr(result, "raw"):
                summary_text = result.raw
            else:
                summary = getattr(result, "summary", None)
                # If summary is an object with 'raw' field, extract it
                if hasattr(summary, "raw"):
                    summary_text = summary.raw
                    # If the raw text is a placeholder, indicate no full summary found
                    if summary_text.strip().lower().startswith("structured soap clinical summary is provided above"):
                        summary_text = "No full summary text found in the output."
                elif summary is not None:
                    summary_text = str(summary)
                else:
                    summary_text = "No summary available."
        if isinstance(summary_text, str):
            summary_text = "Final Output: A complete SOAP-format clinical summary is as follows...\n\n" + summary_text
        return JSONResponse({
            "summary": summary_text,
        })

    except Exception as e:
        # Log exception details for debugging
        error_trace = traceback.format_exc()
        print("Exception in /analyze_audio/:", error_trace)
        return JSONResponse({"error": str(e), "traceback": error_trace}, status_code=500)
    finally:
        # Remove uploaded audio file to keep things tidy
        if os.path.exists(audio_path):
            os.remove(audio_path)
