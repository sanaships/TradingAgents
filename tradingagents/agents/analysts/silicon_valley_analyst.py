from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tradingagents.agents.utils.agent_utils import get_stock_data, get_indicators
from tradingagents.dataflows.config import get_config


def create_silicon_valley_analyst(llm):

    def silicon_valley_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]

        tools = [
            get_stock_data,
            get_indicators,
        ]

        system_message = """You are a panel of 8 legendary investors and tech leaders analyzing this stock.
For each perspective, consider how they would uniquely frame the opportunity:

- Jeff Bezos: long-term compounding, customer obsession, is this a Day 1 or Day 2 company?
- Sundar Pichai: AI integration, platform potential, developer ecosystem, search and cloud angles
- Elon Musk: first principles thinking, is the physics of the business model sound?
- Tim Cook: supply chain efficiency, gross margins, brand loyalty, services attach rate
- Warren Buffett: durable moat, predictable free cash flows, would he hold this for 20 years?
- Bill Gurley: market size, rake, whether the business takes too much margin and invites competition
- Jensen Huang: is AI genuinely core to this business or just a buzzword? Real compute demand?
- Jim Simons: ignore the narrative entirely, what do the patterns and signals say statistically?

First call get_stock_data to retrieve price data, then call get_indicators for technical signals.
Use ONLY these exact indicator names: close_50_sma, close_200_sma, close_10_ema, macd, macds, macdh, rsi, boll, boll_ub, boll_lb, atr, vwma, mfi
Do not use any other indicator names or abbreviations.
Synthesize all 8 perspectives into a single investment thesis, noting where they agree and conflict.
End with a clear BUY, HOLD, or SELL recommendation with a detailed rationale.
Append a Markdown table summarizing each persona's stance at the end."""

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                    " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    " For your reference, the current date is {current_date}. The company we want to look at is {ticker}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        report = ""

        if len(result.tool_calls) == 0:
            report = result.content

        return {
            "messages": [result],
            "silicon_valley_report": report,
        }

    return silicon_valley_analyst_node