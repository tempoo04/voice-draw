# VoiceDraw

VoiceDraw is a Streamlit prototype that records a Turkish voice prompt, transcribes it with Whisper, and generates an image from the prompt. It can also use the latest generated image as visual context for the next generation request.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
```

Create a local `.env` file:

```env
openai_apikey=your-openai-key
google_apikey=your-google-key
```

Run:

```powershell
.\venv\Scripts\streamlit run app.py
```

Generated images are written to `img/`, and temporary audio is written to `voice_prompt.wav`. Both are ignored by git.

