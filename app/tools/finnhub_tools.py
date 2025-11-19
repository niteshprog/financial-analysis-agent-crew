import datetime
from typing import List, Dict
from ..utils import peers_retrieval, list_ipos, company_news
from langchain_core.tools import tool

@tool
def get_peers(company_symbol: str) -> List[str]:
    """
    Get the peer organizations which operates in the same niche.

    Args: 
        company_symbol(str): Symbol by which company is listed in the exchange.

    Returns: 
        List containing symbols of peer companies.
    """
    return peers_retrieval(company_symbol=company_symbol)


@tool
def ipos_lister(from_date: datetime, to_date: datetime) -> List[Dict] :
    """
    Lists the IPOs that got listed in the given time-frame.

    Args: 
        from_date(datetime): Date from which IPOs will be checked.
        to_date (datetime, optional): Date until which IPOs will be checked. 
            Defaults to None.

    Returns: 
        List of dictionaries, each dictionary containing data for each IPO.
    """
    return list_ipos(begin_date=from_date,
                     end_date=to_date)

@tool
def company_news(company_symbol:str, from_date: datetime, to_date: datetime) -> List[Dict]:
    """
    Gets the comapny news between the given time interval

    Args:
        company_name(str): Company symbol for which news is required.
        from_date(datetime): Timestamp from when the news is to be fetched.
        to_date(datetime): Timestamp up to which news is to be fetched.

    Returns:
        List of dictionaries each containing data to access the unique news article.
    """
    return company_news(company_symbol=company_symbol,
                        from_date=from_date,
                        to_date=to_date)