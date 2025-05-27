# herbert ai robot using azure speech 

## what is this
experiments using:
- azure `text to speech` and `speech to text`
- what else...?

## how can i use it?
I want to make a speech based workflow for an ai tool that does stuff I make it do.

[note to self] More details on ideas to build, etc, are on my trello

## todo / done list
Key: this ✅ is done. ⏩ is current WIP. 🔎 is being looked into [substeps for the WIP]. 🕛 is up next.
- ✅ [apr16] set up the repo.
- ✅ [apr23-24] added boilerplate code
- ✅ [apr23-24] tts, stt, llm all work
- ✅ [apr22-23] what parts to buy / use: _AND_ figure out coding workflow **while** we get the parts (trello has the links)
- ✅ [apr23-24] get the azure speech to text code working
- ✅ [apr23-24] get the azure text to speech code working
- ✅ [apr25] get faster-whisper working [going to a new branch for this.]
    - ✅ download faster-whisper ([I'm using THIS MODDED ONE](https://github.com/AIWintermuteAI/WhisperLive.git), video [here](https://www.youtube.com/watch?v=3yLFWpKKbe8))
    - ✅ load it via terminal
- ✅ [apr25] stt working via terminal
- ✅ tts working via terminal
    - ✅ [fixed] [apr27] 🐞bug. my tts is running like 5 times per detected transcibed speech. might need to do threading.
        ```
                Americans have come.
        Running TTS...
        Words extracted for audio name: ['Americans', 'have', 'come']
        audioname______________output\1\americans_have_091336.wav
        TTS completed.
                Americans have come.
        Running TTS...
        Words extracted for audio name: ['Americans', 'have', 'come']
        audioname______________output\1\americans_have_091338.wav
        TTS completed.
                Americans have come.
        Running TTS...
        Words extracted for audio name: ['Americans', 'have', 'come']
        audioname______________output\1\americans_have_091338.wav
        TTS completed.
                Americans have come.
        Running TTS...
        Words extracted for audio name: ['Americans', 'have', 'come']
        audioname______________output\1\americans_have_091339.wav
        TTS completed.
                Americans have come.
        Running TTS...
        Words extracted for audio name: ['Americans', 'have', 'come']
        audioname______________output\1\americans_have_091340.wav
        TTS completed.
        ```
- ✅ llm working via terminal
- ✅✅ ENTIRE PIPELINE working via terminal
- ⏩ sort out some bugs
    - 🐞 llm exceptions aren't handled so they crash the client program in the terminal
    - 🐞 [important] the stt truncates quickly so short pauses break long sentences
        ```Is it common for a Roman jailer? 
          Is it common for a Roman jailer? 
          Is it common for a Roman jayla? 
          Is it common for a Roman jayla? 
          It's prison. 
          this prisoner's home. 
          this prisoner's home and feed them. 
          this prisoner's home and feed them. 
          
          instead of "is it common for a Roman jailer to take his prisoners home and feed them?" 
        ```
- 🕛 figure out how to add gradio / fix gradio stream from mic
- 🕛 load entire workflow via gradio

## previous workflows

### [current] faster-whisper for 'cheap' forever stt.
Load up faster-whisper and run stt forever on one thread. then check for keywords, and run the pipeline from there.
- increased the wait time in `client.py` so that the client doesn't close while the audio response from the LLM is playing.
    - `self.disconnect_if_no_response_for = 60 # 15 MIGISHA changed to 60 seconds`

### [failed] run threads for the vad and stt. then run llm and tts.
This was perfect. but I can't seem to get it to work. I implemented it by calling defs from their files and it double-run the stt. I implemented the defs directly into my main code and it more than double-run the stt - this time it called stt every so often, in a forever loop.
- 🐞 the `def2` (in `main_async.py`) runs twice **sometimes**. I've tried zeroing out the variables so the second run won't succeed but it still runs with knowledge of them. So its call is not normal. I can't find where the bug is coming from.
- 🐞 sometimes azure stt retuns unusable audio and my app crashes.
    ```
    [wav @ 000001ec79e25c40] invalid start code [0][0][0][0] in RIFF header
    [cache @ 000001ec79e261c0] Statistics, cache hits:0 cache misses:0
    [in#0 @ 000001ec79e0b9c0] Error opening input: Invalid data found when processing input
    Error opening input file cache:pipe:0.
    Error opening input files: Invalid data found when processing input
    ```
- 🐞 haven't handled the llm exception when I trigger its `content filter` and it rejects my request.

## 🔎 what parts to buy / use:
- microphone: 
- speaker: 
- amplifier: 
- LEDs: 
- motors / servos for actuation: 
- lisach, start with [this guy](https://www.youtube.com/watch?v=81-zLRHBG0o)

## ideas on how to use it 💡 
1. [note to self] check Trello


## notes
- tried porting exisiting azure code to micropython. Failed. Not enough RAM. Pivot to Pi Zero 2W.![alt text](images/rp2040_out_of_memory.png)