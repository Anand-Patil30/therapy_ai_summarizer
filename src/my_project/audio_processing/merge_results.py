import os
import json
import random

output_dir = "output"

def merge_speaker_segments(segments, max_gap=5.0):
    """Merge adjacent segments from same speaker within max_gap seconds."""
    if not segments:
        return []
    merged = [segments[0].copy()]
    for seg in segments[1:]:
        last = merged[-1]
        if seg["speaker"] == last["speaker"] and (seg["start"] - last["end"] <= max_gap):
            last["text"] += " " + seg["text"]
            last["end"] = seg["end"]
        else:
            merged.append(seg.copy())
    return merged

def merge():
    """
    Load transcript.json and diarization.json, assign speakers to transcript segments,
    merge adjacent same-speaker segments, save final_result_<random>.json
    """
    with open(os.path.join(output_dir, "transcript.json")) as f:
        transcript = json.load(f)
    with open(os.path.join(output_dir, "diarization.json")) as f:
        diarization = json.load(f)

    final_segments = []
    for segment in transcript["segments"]:
        text_start = segment["start"]
        speaker = "unknown"
        for spk in diarization:
            if spk["start"] <= text_start < spk["end"]:
                speaker = spk["speaker"]
                break
        final_segments.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"],
            "speaker": speaker
        })

    merged_segments = merge_speaker_segments(final_segments, max_gap=5)
    filename = f"final_result_{random.randint(1000,9999)}.json"
    save_path = os.path.join(output_dir, filename)

    with open(save_path, "w") as f:
        json.dump(merged_segments, f, indent=2)

    # Cleanup intermediate files
    try:
        os.remove(os.path.join(output_dir, "transcript.json"))
        os.remove(os.path.join(output_dir, "diarization.json"))
    except OSError:
        pass

    print(f"[merge_results] Merged transcript saved to {save_path}")
    return save_path
