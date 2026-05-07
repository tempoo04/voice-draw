"""Shared configuration for VoiceDraw."""
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
ICON_DIR = ROOT_DIR / "icon"
IMAGE_OUTPUT_DIR = ROOT_DIR / "img"
AUDIO_PROMPT_PATH = ROOT_DIR / "voice_prompt.wav"

APP_TITLE = "VoiceDraw"
APP_PAGE_TITLE = "VoiceDraw"
APP_LAYOUT = "wide"

OPENAI_API_KEY_ENV = "openai_apikey"
GOOGLE_API_KEY_ENV = "google_apikey"

OPENAI_IMAGE_MODEL = "dall-e-3"
OPENAI_TRANSCRIPTION_MODEL = "whisper-1"
OPENAI_IMAGE_SIZE = "1024x1024"
OPENAI_IMAGE_QUALITY = "hd"
TRANSCRIPTION_LANGUAGE = "tr"

GEMINI_VISION_MODEL = "gemini-pro-vision"

AUDIO_FORMAT_RATE = 44100
AUDIO_CHANNELS = 1
AUDIO_FRAMES_PER_BUFFER = 1024

