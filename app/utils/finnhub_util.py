"""Serves as the utility module for Finnhub and contains all the utility
methods related to Finnhub."""
import finnhub, datetime
from typing import Optional
from ..core.finnhub_config import FinnHubConfig
from log_util import setup_logger

logger = setup_logger()

class FinnHub(FinnHubConfig):

    def __init__(self):
        super().__init__()
        self.__finnhub_client = self.__get_finnhub_client()

    def __get_finnhub_client(self):

        try:
            return finnhub.Client(api_key=self.finnhub_api_secret)
        except BaseException as e:
            logger.error(msg=e)
            raise BaseException('Auth failed for the Finnhub client.')
    
    def get_peers(self, company_symbol: str): 
        try: 
            peers_list = self.__finnhub_client.company_peers(symbol=company_symbol)
            return peers_list
        except Exception as e: 
            logger.error(msg=e)
            raise BaseException('Failed to get peers for the company.')

    def get_company_news(self, company_symbol: str, begin_date: datetime, end_date: datetime):
        try: 
            formatted_from_date = begin_date.strftime("%Y-%m-%d")
            formatted_to_date = end_date.strftime("%Y-%m-%d")
            company_news = self.__finnhub_client.company_news(symbol=company_symbol, 
                                                              _from=formatted_from_date, 
                                                              to=formatted_to_date)
            return company_news
        except Exception as e: 
            logger.error(msg=e)
            raise BaseException("Failed to get company's news")
        
    def get_basic_financials(self, company_symbol: str, metric = 'all'):
        try: 
            company_basic_financials = self.__finnhub_client.company_basic_financials(symbol=company_symbol,
                                                                                      metric=metric)
            return company_basic_financials
        except Exception as e: 
            logger.error(msg=e)
            raise BaseException('Failed to get financials for the company.')

    def get_company_profile(self, company_symbol: str): 
        try: 
            company_profile = self.__finnhub_client.company_profile2(symbol=company_symbol)
            return company_profile
        except Exception as e:
            logger.error(msg=e) 
            raise BaseException('Failed to get company profile.')

    def get_upcoming_ipos(self,begin_date: datetime, end_date: datetime):
        try: 
            formatted_from_date = begin_date.strftime("%Y-%m-%d")
            formatted_to_date = end_date.strftime("%Y-%m-%d")
            upcoming_ipos = self.__finnhub_client.ipo_calendar(_from=formatted_from_date,
                                                                to=formatted_to_date)
            return upcoming_ipos
        except Exception as e: 
            logger.error(msg=e) 
            raise BaseException('Failed to get upcoming ipos.')
        
    def get_historical_quartely_earnings(self, company_symbol: str, limit: int = None): 
        try: 
            earnings = None
            if limit: 
                earnings = self.__finnhub_client.company_earnings(symbol=company_symbol,
                                                                  limit=limit)
            else: 
                earnings = self.__finnhub_client.company_earnings(symbol=company_symbol)

            return earnings
        except Exception as e: 
            logger.error(msg=e) 
            raise BaseException('Failed to get historical earning for company.')

    def get_visa_applications(self, company_symbol: str, begin_date: datetime, end_date: datetime):
        try: 
            formatted_from_date = begin_date.strftime("%Y-%m-%d")
            formatted_to_date = end_date.strftime("%Y-%m-%d")
            visa_application_details = self.__finnhub_client.stock_visa_application(symbol=company_symbol,
                                                                                    _from=formatted_from_date,
                                                                                    to=formatted_to_date)
            return visa_application_details
        except Exception as e:
            logger.error(msg=e) 
            raise BaseException('Failed to get visa applications.')
        
    def get_reported_financials(self, company_symbol: str, frequency: str = None, access_number: str = None, begin_date: datetime = None, end_date: datetime = None): 
        try: 
            kwargs = {'symbol': company_symbol}

            if frequency: 
                kwargs['freq'] = frequency
            else: 
                kwargs['freq'] = 'annual'
            
            if access_number: 
                kwargs['accessNumber'] = access_number

            if begin_date and end_date: 
                kwargs['_from'] = begin_date.strftime("%Y-%m-%d")
                kwargs['to'] = end_date.strftime("%Y-%m-%d")

            reported_financials = self.__finnhub_client.financials_reported(**kwargs)

            return reported_financials

        except Exception as e: 
            logger.error(msg=e) 
            raise BaseException('Failed to get financials.')
