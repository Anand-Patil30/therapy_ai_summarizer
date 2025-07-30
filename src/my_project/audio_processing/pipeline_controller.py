from audio_processing import stt_transcribe
from audio_processing import diarize_audio
from audio_processing import merge_results

def run_full_pipeline(audio_path):
    """
    Runs the complete pipeline: transcription, diarization, merge.
    Returns the path of the merged output JSON file.
    """
    print("[pipeline_controller] Starting transcription...")
    stt_transcribe.transcribe(audio_path)
    
    print("[pipeline_controller] Starting diarization...")
    diarize_audio.diarize(audio_path)
    
    print("[pipeline_controller] Merging results...")
    merged_path = merge_results.merge()
    
    print(f"[pipeline_controller] Pipeline complete. Output: {merged_path}")
    return merged_path
