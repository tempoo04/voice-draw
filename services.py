"""External AI service helpers used by VoiceDraw."""
import os
from io import BytesIO

import google.generativeai as genai
import PIL.Image
import requests
from dotenv import load_dotenv
from openai import OpenAI

from config import (
    GEMINI_VISION_MODEL,
    GOOGLE_API_KEY_ENV,
    OPENAI_API_KEY_ENV,
    OPENAI_IMAGE_MODEL,
    OPENAI_IMAGE_QUALITY,
    OPENAI_IMAGE_SIZE,
    OPENAI_TRANSCRIPTION_MODEL,
    TRANSCRIPTION_LANGUAGE,
)

load_dotenv()


def _required_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def openai_client():
    return OpenAI(api_key=_required_env(OPENAI_API_KEY_ENV))


def transcribe_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        response = openai_client().audio.transcriptions.create(
            model=OPENAI_TRANSCRIPTION_MODEL,
            file=audio_file,
            language=TRANSCRIPTION_LANGUAGE,
        )
    return response.text


def download_generated_image(prompt):
    response = openai_client().images.generate(
        model=OPENAI_IMAGE_MODEL,
        size=OPENAI_IMAGE_SIZE,
        quality=OPENAI_IMAGE_QUALITY,
        n=1,
        response_format="url",
        prompt=prompt,
    )
    image_url = response.data[0].url
    image_response = requests.get(image_url, timeout=60)
    image_response.raise_for_status()
    return BytesIO(image_response.content)


def describe_image_for_generation(image_path, prompt):
    genai.configure(api_key=_required_env(GOOGLE_API_KEY_ENV))
    multimodality_prompt = f"""Gonderdigim resmi, ek talimatlarla birlikte yeniden olusturmani istiyorum. Once resmi ayrintili tarif et.
Daha sonra bu metnin bir yapay zeka modeliyle gorsel olusturmak icin kullanilacagini dusunerek yanit ver.
Ek talimat: {prompt}"""

    model = genai.GenerativeModel(model_name=GEMINI_VISION_MODEL)
    source_image = PIL.Image.open(image_path)
    response = model.generate_content([multimodality_prompt, source_image])
    response.resolve()
    return response.text

