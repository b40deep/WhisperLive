from whisper_live.client import TranscriptionClient
import os
import time
import subprocess
from texttospeech import get_speech
import re

last_text = ""

def run_generate_audioname(text):
  words = re.findall(r'\b\w{3,}\b', text)
  print(f"Words extracted for audio name: {words}")
  shortened_action_res = "_".join(words[:2]).lower() if words else "audio"
  audioname = f"{shortened_action_res}_{time.strftime('%H%M%S')}"
  return audioname

def run_tts():
  print("Running TTS...")
  global last_text
  get_speech(last_text, audioname=run_generate_audioname(last_text))
  print("TTS completed.")

def sample_callback(text, is_final):
  global last_text
  global client
  if is_final and text != last_text:
    # print("\r" + last_text, end='', flush=True)
    last_text = text[-1]
    print("\t" + last_text)
    client.paused = True
    run_tts()
    client.paused = False
  else:
    # os.system("cls" if os.name == "nt" else "clear")
    # print(last_text, end='', flush=True)
    print("\t" + last_text)

client = TranscriptionClient(
  "localhost",
  9090,
  lang="en",
  translate=False,
  model="tiny.en",
  use_vad=True,
  callback=sample_callback
)

def main():
  global client
  try:
    client()
  except Exception as e:
    print(f"\nExiting... {e}")

if __name__ == "__main__":
  main()

