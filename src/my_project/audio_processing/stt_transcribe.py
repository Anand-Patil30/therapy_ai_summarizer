import whisperx
import json
import os

from my_project.audio_processing import convert_audio

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

def transcribe(audio_path):
    """
    Converts input audio to WAV, transcribes with WhisperX, aligns words.
    Saves transcript.json in output.
    """
    if audio_path.lower().endswith(".wav"):
        wav_path = audio_path
    else:
        wav_path = convert_audio.convert_audio(audio_path)
    print(f"[stt_transcribe] Transcribing {wav_path}...")

    model = whisperx.load_model("base",language="en", device="cpu", compute_type="float32")
    result = model.transcribe(wav_path)

    align_model, metadata = whisperx.load_align_model(language_code="en", device="cpu")
    result = whisperx.align(result["segments"], align_model, metadata, wav_path, device="cpu")

    transcript_path = os.path.join(output_dir, "transcript.json")
    with open(transcript_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"[stt_transcribe] Transcript saved to {transcript_path}")
    return transcript_path
