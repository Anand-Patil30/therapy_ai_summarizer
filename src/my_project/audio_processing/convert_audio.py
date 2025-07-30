import os
from pydub import AudioSegment

def convert_audio(input_file, output_file="output/temp.wav"):
    """
    Convert an input audio file to mono 16kHz WAV format.
    Returns path to the converted file.
    """
    print(f"[convert_audio] Converting {input_file} to WAV 16kHz mono...")
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_frame_rate(16000).set_channels(1)
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    audio.export(output_file, format="wav")
    return output_file
