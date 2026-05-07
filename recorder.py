import wave
import pyaudio

from config import AUDIO_CHANNELS, AUDIO_FORMAT_RATE, AUDIO_FRAMES_PER_BUFFER, AUDIO_PROMPT_PATH


def record(record_active, frames):
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=AUDIO_CHANNELS,
        rate=AUDIO_FORMAT_RATE,
        input=True,
        frames_per_buffer=AUDIO_FRAMES_PER_BUFFER,
    )

    while record_active.is_set():
        data = stream.read(AUDIO_FRAMES_PER_BUFFER, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    sound_file = wave.open(str(AUDIO_PROMPT_PATH), "wb")
    sound_file.setnchannels(AUDIO_CHANNELS)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(AUDIO_FORMAT_RATE)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()
