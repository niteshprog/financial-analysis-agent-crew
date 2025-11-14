"Contains configurations for the Finnhub API"

import os 
from dotenv import load_dotenv


load_dotenv() 

class FinnHubConfig: 
    def __init__(self): 
        self.finnhub_api_secret = os.getenv('FINNHUB_API_SECRET')