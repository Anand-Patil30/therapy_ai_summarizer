import os
import io
import pytest
from fastapi.testclient import TestClient
import sys
import pathlib
from unittest.mock import patch, MagicMock

# Adjust sys.path to import main app correctly
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))

# Mock crewai, dotenv, and python-multipart to avoid import errors during testing
mock_crewai = MagicMock()
sys.modules['crewai'] = mock_crewai
sys.modules['crewai.agent'] = mock_crewai.agent
sys.modules['crewai.agents'] = mock_crewai.agents
sys.modules['crewai.utilities'] = mock_crewai.utilities

mock_dotenv = MagicMock()
sys.modules['dotenv'] = mock_dotenv

mock_multipart = MagicMock()
sys.modules['multipart'] = mock_multipart
sys.modules['python_multipart'] = mock_multipart
sys.modules['fastapi.datastructures'] = MagicMock()
sys.modules['fastapi.datastructures.UploadFile'] = MagicMock()

# Remove mocking fastapi modules to avoid __spec__ is not set error
# sys.modules['fastapi'] = MagicMock()
# sys.modules['fastapi.dependencies'] = MagicMock()
# sys.modules['fastapi.dependencies.utils'] = MagicMock()

from my_project.main import app

client = TestClient(app)

def test_analyze_audio_success():
    # Prepare a small WAV file or use a sample audio file path
    sample_audio_path = os.path.join(os.path.dirname(__file__), "sample.wav")
    # Create a dummy wav file for testing
    with open(sample_audio_path, "wb") as f:
        f.write(b"RIFF$\x00\x00\x00WAVEfmt ")  # minimal WAV header bytes

    with open(sample_audio_path, "rb") as audio_file:
        response = client.post(
            "/analyze_audio/",
            files={"file": ("sample.wav", audio_file, "audio/wav")}
        )
    os.remove(sample_audio_path)
    assert response.status_code == 200
    json_data = response.json()
    assert "summary" in json_data
    assert "merged_transcript" in json_data
    assert "file_name" in json_data

def test_analyze_audio_invalid_file():
    # Send a non-audio file
    response = client.post(
        "/analyze_audio/",
        files={"file": ("test.txt", io.BytesIO(b"not an audio file"), "text/plain")}
    )
    assert response.status_code == 500
    json_data = response.json()
    assert "error" in json_data
    assert "traceback" in json_data
