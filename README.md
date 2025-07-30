# Therapy AI Summarizer

This application is designed to process and analyze audio data for therapy sessions using AI techniques. It includes modules for audio processing, speech-to-text transcription, diarization, and summarization.

## Project Structure

- `src/my_project/audio_processing/`: Contains audio processing scripts such as conversion, diarization, and transcription.
- `src/my_project/tools/`: Custom tools used within the project.
- `src/my_project/config/`: Configuration files for agents and tasks.
- `src/my_project/crew.py` and `src/my_project/main.py`: Main application scripts.
- `knowledge/`: Contains user preferences and other knowledge base files.
- `.gitignore`: Configured to ignore virtual environments (e.g., `therapy/`) and compiled files.

## Setup

1. Create a Python virtual environment (do not commit this folder).
2. Install dependencies listed in `requirements.txt`.
3. Configure any necessary environment variables in a `.env` file (this file should not be committed).

## Usage

Run the main application script:

```bash
uvicorn my_project.main:app --host 0.0.0.0 --port 8000 --reload
```

## Notes

- The virtual environment folder and compiled files are excluded from version control.
- Secrets such as API keys should be stored securely and not committed to the repository.

## License

Specify your license here.
