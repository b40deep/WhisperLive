# Chat with an intelligent assistant in your terminal
# Chat with an intelligent assistant in your terminal
import sys, os
import _models
import json

########################
# TERMINAL COLORS
from terminal_colors import _GRY,_BLU,_PPL,_RED,_GRN,_RST
########################
import os
from openai import AzureOpenAI

# Point to the local server
deployment_name = 'gpt-4o-mini' #This will correspond to the custom name you chose for your deployment when you deployed a model. Use a gpt-35-turbo-instruct deployment. 

bible_json_path = os.path.join('input', 'nkjv_bible.json')
bible_json_file = json.load(open(bible_json_path, 'r'))

def get_bible_book(book_name):
    for book in bible_json_file["books"]:
        if book["name"].lower() == book_name.lower():
            return book
bible_acts = get_bible_book('Acts')

behaviour_config = {
    "Device name": "Commando",
    "response tone": "Respond in third person. Never use human pronouns.",
    "response style": "Use conversational vocabulary, several connected short sentences rather than few long sentences, max 15 words per sentence. maximum 100 words for entire response.",
    "bible tone": "return verses verbatim, ignore verse numbers unless asked for.",
    "bible_reference": bible_acts
}

llm_system_prompt = ". ".join(f"{key}: {value}" for key, value in behaviour_config.items())


history = [
    {"role": "system", "content": f"{llm_system_prompt}"
},
{"role": "user", "content": "What are your instructions? answer in only one sentence. no more."}
]
new_message = {"role": "assistant", "content": ""}

def get_llm_res(prompt):
    print(f"{_GRY}history: {type(history)} | {len(history)}{_RST}")
    client = AzureOpenAI(
        api_key=_models.azure_api_us_key_1,  
        api_version=_models.azure_api_ver,
        azure_endpoint = _models.azure_base_url_us
        )

    # Send a completion call to generate an answer
    print(f'{_BLU} Sending a test completion job {_RST}')
    start_phrase = prompt or 'Write a tagline for an ice cream shop. '
    history.append({"role": "user", "content": start_phrase})

    # response = client.completions.create(model=deployment_name, prompt=start_phrase, max_tokens=10)
    completion = client.chat.completions.create(
                model=deployment_name, 
                # messages = [{"role":"system", "content":start_phrase}],
                messages = history,
                stream=True)

    global new_message
    new_message = {"role": "assistant", "content": ""}

    for chunk in completion:  
        # Each chunk may contain a dictionary with 'choices'  
        if chunk.choices:  
            # if chunk.choices[0]:  
            #     print('__',chunk.choices[0].delta.content)
                # print('__'+chunk.choices[0].delta.content)
            content =  chunk.choices[0].delta.content
            if content:  
                # print(content, end='', flush=True)  # Print the content in real-time  
                new_message["content"] += content
    print(f'{_BLU} LLM RES:{_RST} {_GRY}{new_message["content"]}  {_RST}')
    history.append(new_message)
    return new_message["content"]

def main():
    # print(start_phrase+response.choices[0].text)
    # print(f'{_GRN}  {completion}  {_RST}')
    # print(_GRN + completion.choices[0].message.content + _RST)
    # while True:
    #     print(gen(input(f'{_PPL} User: {_RST}')))

    # print(get_llm_res(f'Tell me a story about Acts 13'))
    # print(get_llm_res(f'Briefly summarize the Islamic religion.'))
    # print(get_llm_res(f'Commando are you there?'))
    print(get_llm_res(f'Commando read Acts 14:2.'))
    # while True:
    #     print(gen(input(f'{_PPL} User: {_RST}')))


if __name__ == "__main__":
    main()
