import os
import random
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

closedai_api_key = os.getenv("CLOSEDAI_API_KEY")
closedai_org = os.getenv("CLOSEDAI_ORG")
closedai_base_url = "https://api.openai.com/v1/chat/completions"

azure_api_uk_key_1 = os.getenv("AZURE_API_UK_KEY_1")
azure_api_us_key_1 = os.getenv("AZURE_API_US_KEY_1")
azure_api_key_phi = os.getenv("AZURE_API_KEY_PHI")
azure_api_ver = os.getenv("AZURE_API_VER") # "request not found" without this!
azure_base_url_uk = "https://kebela-openai.openai.azure.com/"
azure_base_url_us = "https://gezaako.openai.azure.com/"
azure_base_url_phi = "https://ai-21322494914ai090460908350.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview"
# azure_base_url_phi = "https://ai-21322494914ai090460908350.services.ai.azure.com/"

rag_endpoint = os.getenv("RAG_ENDPOINT_URL")  
rag_deployment = os.getenv("RAG_DEPLOYMENT_NAME")  
rag_search_endpoint = os.getenv("RAG_SEARCH_ENDPOINT")  
rag_search_key = os.getenv("RAG_SEARCH_KEY")  
rag_search_index = os.getenv("RAG_SEARCH_INDEX_NAME")  
rag_subscription_key = os.getenv("RAG_AZURE_API_US_KEY_1")  
rag_api_version = "2024-05-01-preview"

tts_speech_key = os.getenv("SPEECH_KEY")
tts_speech_region = os.getenv("SPEECH_REGION")

hf_api_key = os.getenv("HF_API_KEY")

llm={
        "gpt-35-turbo-16k":{"name":"gpt-35-turbo-16k",
        "base_url": f"{azure_base_url_us}",
        "api_key": f"{azure_api_us_key_1}",
        "api_ver": "2024-08-01-preview",
        "org": f"{closedai_org}",
        "online":True
        },
        "gpt-4":{"name":"gpt-4",
        "base_url": f"{azure_base_url_us}",
        "api_key": f"{azure_api_us_key_1}",
        "api_ver": "2024-08-01-preview",
        "org": f"{closedai_org}",
        "online":True
        },
        "gpt-4o-mini":{"name":"gpt-4o-mini",
        "base_url": f"{azure_base_url_us}",
        "api_key": f"{azure_api_us_key_1}",
        "api_ver": "2024-08-01-preview",
        "org": f"{closedai_org}",
        "online":True
        },
        "Phi-3.5-MoE-instruct":{"name":"Phi-3.5-MoE-instruct",
        "base_url": azure_base_url_phi,
        "api_key": f"{azure_api_key_phi}",
        "api_ver": "2024-05-01-preview",
        "org": None,
        "online":True
        },
        "Phi-3-medium-128k-instruct":{"name":"Phi-3-medium-128k-instruct",
        "base_url": azure_base_url_phi,
        "api_key": f"{azure_api_key_phi}",
        "api_ver": "2024-05-01-preview",
        "org": None,
        "online":True
        },
        "dolphin-2.2.1-mistral-7B":{"name":"TheBloke/dolphin-2.2.1-mistral-7B-GGUF",
        "base_url":"http://localhost:1234/v1",
        "api_key":"lm-studio",
        "org": "",
        "online":False
        }
    }

llm_temperature = 0.7
llm_neg_prompts ='bad, worse, ugly, nsfw,' #not yet used
t2i_neg_prompts ='bad, worse, ugly, nsfw, speech bubbles' #not yet used

t2i={
        
        "dall-e-2" : {"name":"dall-e-2",
        "base_url": "https://gezaako.openai.azure.com/openai/deployments/dall-e-2/images/generations?api-version=2024-02-01",
        "api_key": azure_api_us_key_1,
        "api_ver": "2024-02-01",
        "org": closedai_org,
        "online":True
        },
        "dall-e-3" : {"name":"dall-e-3",
        "base_url": "https://gezaako.openai.azure.com/openai/deployments/dall-e-3/images/generations?api-version=2024-02-01",
        "api_key": azure_api_us_key_1,
        "api_ver": "2024-02-01",
        "org": closedai_org,
        "online":True
        },
        "dreamshaper-xl" :{"name":"dreamshaper-xl",
        "base_url": "127.0.0.1:8188",
        # "base_url": " 581962c484bb02cb0a.gradio.live",
        "api_key": '',
        "org": '',
        "online":False
        }
    }

t2i_img_size_options = ["1024x1024","512x512"]
t2i_img_size_info = "256x256, 512x512, or 1024x1024 for dall-e-2; 1024x1024, 1792x1024, or 1024x1792 for dall-e-3"
t2i_img_size = t2i_img_size_options[0]
t2i_img_quality_options =["standard","hd"] # hd only works with OpenAI Dall-e 3
t2i_img_quality = t2i_img_quality_options[0]
t2i_num_of_imgs =1
t2i_seed = random.randint(1,100000)

SAVE_LOCATION = os.path.join('march_study','output') #updated from march_batch.py

selected_llm = llm['gpt-4o-mini']
selected_t2i = t2i['dreamshaper-xl']
