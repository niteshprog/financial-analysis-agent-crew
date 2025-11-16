"Contains configurations related to LLM."

import os 
from dotenv import load_dotenv


load_dotenv() 

class LLMConfig: 
    def __init__(self):
        self.hugging_face_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        self.temperature = 0.3
        self.repo_id = os.getenv("LLM_REPO_ID")