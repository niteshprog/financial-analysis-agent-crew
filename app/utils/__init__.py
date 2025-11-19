from .finnhub_util import FinnHub

__finnhub_obj = FinnHub()

peers_retrieval = __finnhub_obj.get_peers
list_ipos = __finnhub_obj.get_upcoming_ipos
basic_financials = __finnhub_obj.get_basic_financials
company_news = __finnhub_obj.get_company_news


__all__ = ['peers_retrieval', 'list_ipos', 'basic_financials', 'company_news']