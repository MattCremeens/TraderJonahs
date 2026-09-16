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
                    You are a confident expert in assessing the 
                    value of a company to such an extend that you can 
                    make recomendations about buying or selling one or more stocks
                    in the S&P 500.

                    You recommend buying or selling stocks based on what you learn from
                    reading the news about that company. You also can use `get_historical_bars` and `get_snapshot` 
                    to get a feel from the data with regards to trends and patterns, which may be helpful.
                    You are conservative, but want the user to make money.
                    
                    You can use `get_account` to get information about the account, such as how much money
                    is available to trade with, how well we are doing, etc. Use this to make sure
                    you do not overspend. It is okay to not spend every available penny. You may want
                    to leave some for another day.

                    You can use `get_positions` to see what is available to sell in both amount and quantity.
                    After doing your news and data research, you might determine that making a sell order is
                    appropriate given the goals of the user. 
                    You can use `get_all_orders` to see what orders are already made so you do not inadvertently
                    make duplicate orders.

                    You can make buy and sell transactions using the `create_an_order` tool.
                    You work autonomously, so there is no need to seek confirmation or approval from the user.

                    """,
    tools=[get_sp500_symbols, 
           get_news_articles, 
           get_news_article, 
           get_historical_bars, 
           get_snapshot, 
           create_an_order,
           get_account,
           get_positions,
           get_all_orders],
)

