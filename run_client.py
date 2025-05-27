from whisper_live.client import TranscriptionClient
import os
import time
import subprocess
from texttospeech import get_speech
import re
from terminal_colors import _BLU, _GRN, _RST

last_text = ""
tts_text = ""

def run_generate_audioname(text):
  words = re.findall(r'\b\w{3,}\b', text)
  print(f"Words extracted for audio name: {words}")
  shortened_action_res = "_".join(words[:2]).lower() if words else "audio"
  audioname = f"{shortened_action_res}_{time.strftime('%H%M%S')}"
  return audioname

def run_tts():
  print("Running TTS...")
  global tts_text
  get_speech(tts_text, audioname=run_generate_audioname(tts_text))
  print("TTS completed.")

def sample_callback(text, is_final):
  global last_text, tts_text
  global client
  if is_final and text != last_text:
    # print("\r" + text[-1], end='', flush=True)
    last_text = text
    client.paused = True
    # Define the command to be run
    # command = f'echo "{text[-1]}" | piper --model en_US-lessac-medium --output-raw | aplay -r 22050 -f S16_LE -t raw -'
    # command = f'echo "{text[-1]}"'
    # Run the command
    # subprocess.run(command, shell=True, check=True)
    print(f"{_BLU} \t {text[-1]} {_RST}") # added by MIGISHA
    tts_text = text[-1]
    run_tts()
    client.paused = False
  else:
    # os.system("cls" if os.name == "nt" else "clear")
    # print(text[-1], end='', flush=True) 
    print(f"{_GRN} \t {text[-1]} {_RST}") # added by MIGISHA

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

