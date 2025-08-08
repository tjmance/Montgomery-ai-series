import os, json, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
TTS = os.getenv("TTS_HOST", "http://127.0.0.1:5002")
SCENE = Path("scenes/ep01_the_static")
DIALOGUE = json.loads(Path("prompts/dialogue.json").read_text())
AUDIO_DIR = SCENE/"audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

voices = {
  "MARCUS": os.getenv("VOICE_MARCUS", "en_US/vctk_low"),
  "ANGELA": os.getenv("VOICE_ANGELA", "en_US_v2")
}

def tts(line, voice, out):
  r = requests.get(f"{TTS}/api/tts", params={"text": line, "voice": voice, "vocoder": "hifigan"})
  r.raise_for_status()
  (AUDIO_DIR/out).write_bytes(r.content)

if __name__ == "__main__":
  idx = 0
  for beat in DIALOGUE.get("diner_banter", []):
    spk, line = beat["speaker"], beat["line"]
    out = f"dialogue_{idx:02d}_{spk}.wav"
    tts(line, voices[spk], out)
    idx += 1
