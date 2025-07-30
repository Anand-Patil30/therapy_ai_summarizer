import os
import json
from pyannote.audio import Pipeline

from my_project.audio_processing import convert_audio

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

def diarize(audio_path):
    """
    Converts audio to mono 16kHz wav, runs pyannote diarization,
    saves diarization.json in output.
    Requires HF_TOKEN env variable to be set.
    """
    if audio_path.lower().endswith(".wav"):
        wav_path = audio_path
    else:
        wav_path = convert_audio.convert_audio(audio_path)
    print(f"[diarize_audio] Running diarization on {wav_path}...")

    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        raise ValueError("HF_TOKEN environment variable is not set. Please set it to your Hugging Face API token.")
    try:
        print("Entered try block/n/n")
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=hf_token)
        pipeline.embedding_batch_size = 1
    except Exception as e:
        raise RuntimeError(f"Failed to load diarization pipeline: {e}")
    diarization = pipeline(wav_path)

    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker
        })

    diarization_path = os.path.join(output_dir, "diarization.json")
    with open(diarization_path, "w") as f:
        json.dump(segments, f, indent=2)
    print(f"[diarize_audio] Diarization saved to {diarization_path}")
    return diarization_path
