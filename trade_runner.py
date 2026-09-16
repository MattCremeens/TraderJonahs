import asyncio
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent


async def main():
    app_name = "TraderJonah"
    user_id = "Jonah"
    session_id = str(uuid.uuid4())

    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )

    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service,
    )

    user_query = """
    Take a look at my portfolio as well as some stocks not currently in my
    portfolio and analyze them by looking at their historical data as well
    as relevant news articles.

    With this analysis, assess whether to buy, sell, or hold the stocks you
    are examining.

    Do not spend more than $1,000 or the amount in my account, whichever is
    less, while making purchases.
    """

    message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_query)],
    )

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
    ):
        pass


if __name__ == "__main__":
    asyncio.run(main())