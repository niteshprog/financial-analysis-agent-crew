from .finnhub_config import FinnHubConfig
from .llm_config import LLMConfig

__finnhub_config = FinnHubConfig()
__llm_config = LLMConfig()

finnhub_params = __finnhub_config
llm_params = __llm_config

__all__ = ['finnhub_params', 'llm_params']