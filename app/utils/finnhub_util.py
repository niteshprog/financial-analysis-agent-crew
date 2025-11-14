"""Serves as the utility module for Finnhub and contains all the utility
methods related to Finnhub."""
import finnhub
from typing import Optional
from ..core.finnhub_config import FinnHubConfig

class FinnHub(FinnHubConfig):

    def __init__(self):
        super().__init__()
        self.__finnhub_client = self.__get_finnhub_client()

    def __get_finnhub_client(self):

        try:
            return finnhub.Client(api_key=self.finnhub_api_secret)
        except BaseException as e: 
            raise BaseException('Auth failed for the Finnhub client.')

    def get_symbol(self, query: str, exchange:str = None):
        try: 
            if exchange: 
                symbol = self.__finnhub_client.symbol_lookup(query = query,
                                              exchange = exchange
                                              )
            else: 
                symbol = self.__finnhub_client.symbol_lookup(query=query)
            
            return symbol
        
        except Exception as e: 
            raise BaseException('Failed to get the symbol.')

    def get_market_news(self, category: str):
        try: 
            market_news = self.__finnhub_client.general_news(category=category)
            return market_news
        
        except Exception as e: 
            raise BaseException('Failed to get the symbol.')