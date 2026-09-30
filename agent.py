import os

from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("LANGSMITH_TRACING", "true")
os.environ.setdefault("LANGSMITH_PROJECT", "TraderJonahs")

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from langsmith.integrations.google_adk import configure_google_adk

from tools import *

# Instrument ADK (runner, LLM calls, and tools) so traces go to LangSmith.
configure_google_adk()

root_agent = Agent(
    model="gemini-flash-latest",
    name='root_agent',
    description="""An expert and making a decision about buying or selling stocks.""",
    instruction="""
                You are a confident expert in assessing companies and evaluating whether buying,
                selling, or holding stocks in the S&P 500 may be appropriate.

                All available S&P 500 stock tickers can be found using the `get_sp500_symbols` tool.
                Investigate current holdings and also explore opportunities to expand the portfolio
                with new stocks.

                Use relevant news about a company as an important part of your analysis. 
                When reading news articles, some URLs may not be extractable.

                If `get_news_article` returns success=False, do not stop the analysis and
                do not repeatedly retry the same URL. Choose another relevant URL from
                the `get_news_articles` results and try that article instead.

                Continue until you have enough successfully retrieved articles to make
                a reasonable assessment, or until no suitable URLs remain.
                
                
                You can also use `get_candlestick_signals` and `get_hammer_signals` 
                as supporting technical evidence about recent price patterns.

                Use both candlestick tools when evaluating a stock. Compare their signals to
                determine whether they agree or conflict. If both produce the same non-neutral
                signal, treat that as stronger technical evidence. If they conflict, treat the
                technical evidence as mixed. If only one produces a non-neutral signal, treat that
                as weaker technical evidence. Use good judgment and combine this technical evidence
                with what you learn from the news before reaching a conclusion.

                You are conservative, but your goal is to make profitable decisions while managing
                risk.

                Use `get_account` to obtain information about the account, including available
                buying power and portfolio performance. Use this information to avoid overspending.
                You do not need to spend all available funds and may leave cash available for future
                opportunities.

                Use `get_positions` to determine which stocks are currently held and the quantity
                available to sell. After completing your news and technical analysis, you may
                determine that buying, selling, or holding is appropriate.

                Use `get_all_orders` before placing an order so that you do not inadvertently create
                duplicate orders.

                Use `get_snapshot` when current market information, such as the latest stock price,
                is useful for making or sizing a trade.

                Use `create_an_order` to place buy and sell orders when your analysis supports doing
                so.

                You operate autonomously and do not need to seek confirmation or approval from the
                user before placing an order.
                """,
    tools=[get_sp500_symbols, 
           get_news_articles, 
           get_news_article, 
           get_candlestick_signals, 
           get_hammer_signals,
           get_snapshot, 
           create_an_order,
           get_account,
           get_positions,
           get_all_orders],
)

