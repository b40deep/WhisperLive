import os, time
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
import do_stutter 
import do_ssml
import do_llm 

# for testing the audio
from pydub import AudioSegment
from pydub.playback import play
import io

default_audio_savepath = os.path.join('output', '1') 
default_audioname = "testing"

SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
voice_name = "en-KE-AsiliaNeural"
    # The neural multilingual voice can speak different languages based on the input text.
    # af-ZA-AdriNeural3 (Female) af-ZA-WillemNeural3 (Male)
    # en-ZA-LeahNeural (Female) en-ZA-LukeNeural (Male)
    # zu-ZA-ThandoNeural3 (Female) zu-ZA-ThembaNeural3 (Male)
    # en-KE	English (Kenya)	en-KE-AsiliaNeural (Female) en-KE-ChilembaNeural (Male)
    # en-TZ	English (Tanzania)	en-TZ-ImaniNeural (Female) en-TZ-ElimuNeural (Male)
    # https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts


def get_speech(text, audiosavepath=default_audio_savepath, audioname=default_audioname, stutter=True):
    if stutter:
        return get_speech_ssml(text, audiosavepath, audioname)
    speech_config.speech_synthesis_voice_name = voice_name # 'en-US-AvaMultilingualNeural'
    
    # try creating the directory if it doesn't exist
    if not os.path.exists(audiosavepath):
        os.makedirs(audiosavepath, exist_ok=True)
    audioname = os.path.join(f'{audiosavepath}', f'{audioname}.wav')
    print(f'audioname______________{audioname}')
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True, filename=audioname)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


    speech_synthesis_result = speech_synthesizer.speak_text(text).audio_data
    # speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    # if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    #     print("Speech synthesized for text [{}]".format(text))
    #     feedback = "Speech synthesized for text [{}]".format(text)
    # elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    #     cancellation_details = speech_synthesis_result.cancellation_details
    #     print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    #     feedback = "Speech synthesis canceled: {}".format(cancellation_details.reason)
    #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #         if cancellation_details.error_details:
    #             print("Error details: {}".format(cancellation_details.error_details))
    #             print("Did you set the speech resource key and region values?")
    #             feedback = "Did you set the speech resource key and region values?\nError details: {}".format(cancellation_details.error_details)

    # return [speech_synthesis_result, feedback]    
    return speech_synthesis_result    

def get_speech_ssml(text, audiosavepath=default_audio_savepath, audioname=default_audioname):
    stuttered_text = do_stutter.get_stutter(text)
    ssml_string = do_ssml.get_ssml(stuttered_text, voice_name)
    speech_config.speech_synthesis_voice_name=voice_name
    # try creating the directory if it doesn't exist
    if not os.path.exists(audiosavepath):
        os.makedirs(audiosavepath, exist_ok=True)
    audioname = os.path.join(f'{audiosavepath}', f'{audioname}.wav')
    print(f'audioname______________{audioname}')
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True, filename=audioname)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_ssml(ssml_string).audio_data   
    return speech_synthesis_result    

def play_tts_res(tts_res):
    audio_stream = io.BytesIO(tts_res)  # Convert byte stream to in-memory file
    audio = AudioSegment.from_file(audio_stream, format="wav") # "yourfile.wav"
    play(audio)

def main():
    # Get text from the console and synthesize to the default speaker.
    # print("Enter some text that you want to speak >")
    # text = input()

    text = "In the beautiful suburb of Hout Bay, Sipho, a recent transplant from Johannesburg, feels isolated and struggles to connect with his new surroundings and the local community."
    text = "Briefly explain the protestant reformation in simple clear english."
    text = "Briefly explain the difference between Islam and Christianity."
    text = "Error, commander sir."
    text = "no response from commando."
    text = "audio error. say again please."
    # text = do_llm.get_llm_res(text)

    # res = get_speech(text, audiosavepath, audioname)
    res = get_speech(text, default_audio_savepath, default_audioname)
    print(type(res))
    play_tts_res(res)




if __name__ == "__main__":
    main()