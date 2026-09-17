import os
from io import StringIO

import pandas as pd
import requests
from dotenv import load_dotenv
from langsmith import traceable
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv('ALPACA_API_KEY')
secret_key = os.getenv('ALPACA_SECRET_KEY')
tavily_key = os.getenv('TAVILY_API_KEY')
tavily_client = TavilyClient(api_key=tavily_key)


# Alpaca

@traceable(run_type="tool")
def get_account() -> dict:
    """
    Use this tool to get account information. This should tell you how much money
    is available to trade with, how well we are doing, etc. Use this to make sure
    you do not overspend. It's okay to not spend every available penny. You may want
    to leave some for another day.

    Args:
        None
    Returns:
        A dictionary of the account information.
    """


    url = "https://paper-api.alpaca.markets/v2/account"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key
    }

    response = requests.get(url, headers=headers)

    return response.json()

@traceable(run_type="tool")
def get_positions() -> list[dict]:
    """Use this tool to determine what is available to sell in both amount and quantity.
    
    Args:
        None
    Returns:
        A list of dictionaries, each containing the position information for a stock.
    """

    url = "https://paper-api.alpaca.markets/v2/positions"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key
    }

    response = requests.get(url, headers=headers)

    return response.json()

@traceable(run_type="tool")
def get_all_orders() -> list[dict]:
    """Use this tool to be aware of orders already made.
    
    Args:
        None
    Returns:
        A list of dictionaries, each containing the order information for an order.
    """

    url = "https://paper-api.alpaca.markets/v2/orders"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key
    }

    response = requests.get(url, headers=headers)

    return response.json()
    
    
@traceable(run_type="tool")
def get_news_articles(symbol: str) -> list[str]:
    """
    Use this tool in order to learn what news articles on a specific company are available.

    Args:
        symbol: The symbol of the company to research.

    Returns:
        A list of URLs to the news articles about the company.
    """
    article_urls = []
    url = f"https://data.alpaca.markets/v1beta1/news?sort=desc&symbols={symbol}"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key
    }

    response = requests.get(url, headers=headers)
    for article in response.json()['news']:
        article_urls.append(article['url'])

    return article_urls

@traceable(run_type="tool")
def get_historical_bars(symbol: str, timeframe: str, start: str, end: str, limit: str) -> dict:
    """
    Use this tool to get the historical bars for a specific company.
    It is useful when you want to gather evidence to help you determine whether 
    to buy or sell a stock and how much to buy or sell.

    For timeframe, The timeframe represented by each bar in aggregation.
    You can use any of the following values:

    [1-59]Min or [1-59]T, e.g. 5Min or 5T creates 5-minute aggregations
    [1-23]Hour or [1-23]H, e.g. 12Hour or 12H creates 12-hour aggregations
    1Day or 1D creates 1-day aggregations
    1Week or 1W creates 1-week aggregations
    [1,2,3,4,6,12]Month or [1,2,3,4,6,12]M, e.g. 3Month or 3M creates 3-month aggregations


    Args:
        symbol: The symbol of the company to research.
        timeframe: The timeframe of the bars to get.
        start: The start date of the bars to get.
        end: The end date of the bars to get. Day must be less than today's date.
        limit: The limit of the bars to get.
    Returns:
        A dictionary of the historical bars for the company.
    """
    url = f"https://data.alpaca.markets/v2/stocks/{symbol}/bars?timeframe={timeframe}&start={start}&end={end}&limit={limit}&adjustment=raw&feed=sip&sort=asc"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key
    }

    response = requests.get(url, headers=headers)

    return response.json()

@traceable(run_type="tool")
def get_snapshot(symbol: str) -> dict:
    """
    Use this tool to get the snapshot for a specific company.
    The snapshot includes the latest price, volume, and other information.
    It is useful when you want to gather evidence to help you determine whether 
    to buy or sell a stock and how much to buy or sell.
    Args:
        symbol: The symbol of the company to get the snapshot for.
    Returns:
        A dictionary of the snapshot.
    """

    url = f"https://data.alpaca.markets/v2/stocks/{symbol}/snapshot"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key
    }

    response = requests.get(url, headers=headers)

    return response.json()

@traceable(run_type="tool")
def create_an_order(symbol: str, side: str, qty: int) -> dict:
    """
    Use this tool to make an order to buy or sell a stock with a given symbol.
    side may be "buy" or "sell" only. qty is the number of shares to buy or sell.
    Args:
        symbol: The symbol of the company to order.
        side: The side of the order to make (buy or sell)
        qty: The number of shares to buy or sell (can be fractional).
    Returns:
        A dictionary of the order.
    """
    url = "https://paper-api.alpaca.markets/v2/orders"

    payload = {
        "time_in_force": "day",
        "type": "market",
        "symbol": symbol,
        "qty": qty,
        "side": side
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.text

# Tavily
@traceable(run_type="tool")
def get_news_article(url: str) -> str:
    """
    Use this tool when you want to research a company in order to help you 
    make a decision about whether to buy or sell a stock.

    Args:
        url: The URL of the news article to research.

    Returns:
        The raw content of the news article.
    """
    response = tavily_client.extract(url)
    return response['results'][0]['raw_content']

# All symbols
@traceable(run_type="tool")
def get_sp500_symbols() -> list[str]:
    """
    Use this tool to get a list of all of the symbols that make up the S&P 500.
    The total length of the list should be around 500.
    Args:
        None
    Returns:
        A list of all of the symbols that make up the S&P 500.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    table = pd.read_html(StringIO(response.text))[0]

    return [
        symbol.replace(".", "-")
        for symbol in table["Symbol"].tolist()
    ]
