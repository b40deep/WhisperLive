# format the given text as ssml
# text will come as a string
# example "In the beautiful ||sə||suburb|| of Hout Bay, Sipho, a recent transplant from ||ʤo||Johannesburg,|| feels isolated and struggles to ||kɑ||connect|| with his new surroundings and the local community."
# then converts it to ssml. 


############################################
# SSML NOTES
############################################
# SSML with phoneme-level pronunciation
            # <emphasis level="strong">hello</emphasis> 
            # <prosody pitch="+10%">hello world</prosody>
# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-structure
############################################
# STRUCTURE
############################################
# ssml_string = f"""
#     <speak version="1.0" xml:lang="en-US">
#         <voice name="en-KE-AsiliaNeural">
#             <prosody pitch="low"><emphasis level="reduced"><phoneme alphabet="ipa" ph="ha">hello</phoneme></emphasis></prosody> \
#             <break time="0ms"/> \
#             <prosody pitch="high">hello-</prosody>
#             <prosody pitch="low">world!</prosody>
#             Here is a story for you.
#         </voice>
#     </speak>
#     """
############################################

import re

def get_ssml(text: str, voice_name: str) -> str:
    """
    Converts the given text into SSML format by extracting phonemes from stuttered words.
    """
    # Regular expression to match stuttered words (||phoneme||word||)
    pattern = r"\|\|(.*?)\|\|(.*?)\|\|"

    # Replace stuttered words with SSML formatting
    def replace_match(match):
        phoneme, s_word = match.groups()
        return f"""\
            <prosody pitch="low"><emphasis level="reduced"><phoneme alphabet="ipa" ph="{phoneme}">x</phoneme></emphasis></prosody> \
            <break time="0ms"/> \
            <prosody pitch="low"><emphasis level="reduced"><phoneme alphabet="ipa" ph="{phoneme}">x</phoneme></emphasis></prosody> \
            <break time="0ms"/> \
            <prosody pitch="high">{s_word}</prosody> \
        """

    # Apply regex substitution to the text
    formatted_text = re.sub(pattern, replace_match, text)

    # Wrap in SSML structure
    ssml_output = f"""
    <speak version="1.0" xml:lang="en-US">
        <voice name="{voice_name}">
            {formatted_text}
        </voice>
    </speak>
    """
    return ssml_output.strip()

def main():
    # Example usage
    text = "In the beautiful ||sə||suburb|| of Hout Bay, Sipho, a recent transplant from ||ʤo||Johannesburg,|| feels isolated and struggles to ||kɑ||connect|| with his new surroundings and the local community."
    voice_name = "en-US-JennyNeural"

    ssml_result = get_ssml(text, voice_name)
    print(ssml_result)

if __name__ == "__main__":
    main()