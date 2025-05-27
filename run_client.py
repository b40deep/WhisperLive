from whisper_live.client import TranscriptionClient
import os
import time
import subprocess
from texttospeech import get_speech
from do_llm import get_llm_res
import re
from terminal_colors import _BLU, _GRN, _GRY, _RST
from pydub import AudioSegment
from pydub.playback import play
import io

last_text = ""
stt_res = ""
action_res = ("", "")  # Initialize action_res as a tuple
yes_commander_path = os.path.join("input","yes_commander_sir.wav")
the_white_paper_path = os.path.join("input","the_white_paper.wav")
no_llm_res_path = os.path.join("input","no_llm_res.wav")
error_path = os.path.join("input","error.wav")
audio_error_path = os.path.join("input","audio_error.wav")
yes_commander_file = AudioSegment.from_file(yes_commander_path, format="wav")
the_white_paper_file = AudioSegment.from_file(the_white_paper_path, format="wav")
no_llm_res_file = AudioSegment.from_file(no_llm_res_path, format="wav") 
error_file = AudioSegment.from_file(error_path, format="wav")
audio_error_file = AudioSegment.from_file(audio_error_path, format="wav")


def get_action():
  global stt_res
  # def for action based on STT result
  print(f"{_GRY}Parsing Action based on STT result.{_RST}")
  # then check the stt result for ketchphrases
  # switch case for the keyphrases
  stt_res = stt_res.lower().strip()  # Normalize the STT result
  # action_res will now hold a tuple: (action_type, value)
  if "hey commando" in stt_res:
      action_res = ("yes_commander_sir", "Yes commander Sir. Computer izi ready for duty Sir. Yes sir mister sir!")
  elif "white paper bad" in stt_res:
      action_res = ("the_white_paper", "The white paper is bad because the white paper is against non-whites!")
  # do not understand if input is not clear
  elif stt_res == "" or len(stt_res.split()) < 3:
      action_res = ("sibitegeela", "I do not understand. Please clarify your command.")
  # final / default case is to do not understand if llm prompt is not clear
  else:
      action_res = ("llm_prompt", stt_res)  # Send other cases to LLM
  return action_res

def run_generate_audioname(text):
  words = re.findall(r'\b\w{3,}\b', text)
  print(f"{_GRY}Words extracted for audio name: {words}{_RST}")
  shortened_action_res = "_".join(words[:2]).lower() if words else "audio"
  audioname = f"{shortened_action_res}_{time.strftime('%H%M%S')}"
  return audioname

def play_audio(audio):
    play(audio)
    print(f"{_GRY}🛑 Audio finished or stopped!{_RST}")

def play_tts_res(tts_res):
  try:
    audio_stream = io.BytesIO(tts_res)  # Convert byte stream to in-memory file
    audio = AudioSegment.from_file(audio_stream, format="wav")  # Load audio from byte stream
    print(f"{_GRY}Audio generation done{_RST}")
    play_audio(audio)  # Play the audio
  except Exception as e:
    print(f"{_GRY}Error playing TTS result: {e}{_RST}")
    play_audio(audio_error_file)

def run_tts():
  print("Running TTS...")
  global stt_res
  get_speech(stt_res, audioname=run_generate_audioname(stt_res))
  print("TTS completed.")

def sample_callback(text, is_final):
  global last_text, stt_res, action_res
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
    stt_res = text[-1]
    action_res = get_action()  # Get the action based on STT result
    # now ping the llm if the res says so
    if action_res[0] == "llm_prompt":
        llm_res = get_llm_res(action_res[1])
        if llm_res.strip() == "" or len(llm_res.split()) < 2:
          play_audio(no_llm_res_file)
        else:
          tts_input = llm_res
          print(f"{_GRY}LLM result / TTS input: {tts_input}{_RST}")
          # after the llm, do tts
          if tts_input:
              shortened_action_res = "_".join(re.findall(r'\b\w{3,}\b', action_res[1])[:2]).lower()
              audioname = f"{shortened_action_res}_{time.strftime('%H%M%S')}"
              tts_res = get_speech(text=tts_input, audioname=audioname)
              print(f"{_GRY}TTS result: playing...{_RST}")
              play_tts_res(tts_res)
              # time.sleep(1)  # Pause before stopping
    elif action_res[0] == "yes_commander_sir":
        play_audio(yes_commander_file)
    elif action_res[0] == "the_white_paper":
        play_audio(the_white_paper_file)
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

