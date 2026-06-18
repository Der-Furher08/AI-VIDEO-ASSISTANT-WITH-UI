import whisper
import os
import requests
import subprocess

SARVAM_PIECE_SECONDS = 25
WHISPER_MODEL = os.getenv("WHISPER_MODEL","tiny")

_model = None

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_STT_TRANSLATE_URL = "https://api.sarvam.ai/speech-to-text-translate"
SARVAM_MODEL = os.getenv("SARVAM_STT_MODEL", "saaras:v2.5")

def load_model():
    global _model

    if _model is None:
        print(f"loading model...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("whisper model load successfully")

    return _model

def transcribe_chunk_whisper(chunk_path: str) -> str:
    model = load_model()
    result = model.transcribe(chunk_path, task="transcribe")
    return result["text"]

def _send_to_sarvam(piece_path: str) -> str:
    """Send one ≤30s WAV file to Sarvam and return the English transcript."""
    headers = {"api-subscription-key": SARVAM_API_KEY}

    with open(piece_path, "rb") as f:
        files = {"file": (os.path.basename(piece_path), f, "audio/wav")}
        data = {"model": SARVAM_MODEL, "with_diarization": "false"}
        response = requests.post(
            SARVAM_STT_TRANSLATE_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=120,
        )

    if not response.ok:
        print(f"\n❌ Sarvam returned {response.status_code}")
        print(f"Response body: {response.text}\n")
        response.raise_for_status()

    return response.json().get("transcript", "")

def transcribe_chunk_sarvam(chunk_path: str) -> str:
    if not SARVAM_API_KEY:
        raise RuntimeError("SARVAM_API_KEY is not set")

    temp_dir = f"{chunk_path}_sarvam_parts"
    os.makedirs(temp_dir, exist_ok=True)

    output_pattern = os.path.join(temp_dir, "part_%03d.wav")

    subprocess.run(
        [
            "ffmpeg",
            "-i",
            chunk_path,
            "-f",
            "segment",
            "-segment_time",
            str(SARVAM_PIECE_SECONDS),
            "-c",
            "copy",
            output_pattern,
            "-y",
        ],
        check=True,
    )

    pieces = sorted(
        [
            os.path.join(temp_dir, f)
            for f in os.listdir(temp_dir)
            if f.endswith(".wav")
        ]
    )

    full_text = ""

    for i, piece_path in enumerate(pieces):
        print(f"  → Sarvam piece {i + 1}/{len(pieces)} ...")

        try:
            full_text += _send_to_sarvam(piece_path) + " "
        finally:
            if os.path.exists(piece_path):
                os.remove(piece_path)

    try:
        os.rmdir(temp_dir)
    except:
        pass

    return full_text.strip()


def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
    """
    Route one chunk to Whisper or Sarvam depending on language choice.
    - english  → Whisper (local model)
    - hinglish → Sarvam (translates to English while transcribing)
    """
    if language.lower() == "hinglish":
        return transcribe_chunk_sarvam(chunk_path)
    return transcribe_chunk_whisper(chunk_path)


def transcribe_all(chunks: list, language: str = "english") -> str:

    full_transcript = "" 

    engine = "Sarvam AI" if language.lower() == "hinglish" else "Whisper"
    print(f"Using {engine} for transcription.")

    for i, chunk in enumerate(chunks):  

        print(f"Transcribing chunk {i + 1}/{len(chunks)}...")

        text = transcribe_chunk(chunk, language=language)  

        full_transcript += text + " "  

    print("Transcription complete.")

    return full_transcript.strip()   
     