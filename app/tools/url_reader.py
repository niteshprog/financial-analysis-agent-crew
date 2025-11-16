import aiohttp
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from langchain.tools import ToolRuntime




async def read_redirected_content(url: str) -> dict:
    """
    Scrape with realistic browser headers to avoid 403 errors.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
    }
    
    try:
        async with aiohttp.ClientSession(auto_decompress=True) as session:
            async with session.get(url, headers=headers, allow_redirects=True) as response:
                
                # final_url = str(response.url)
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                return {
                    'title': soup.title.string if soup.title else 'No title',
                    'content': soup.get_text(separator="\n", strip=True)                
                    }
                
    except Exception as e:
        print(f"Error: {e}")
        return None