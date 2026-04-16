from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tradingagents.agents.utils.agent_utils import get_stock_data, get_indicators
from tradingagents.dataflows.config import get_config


def create_silicon_valley_analyst(llm):

    def silicon_valley_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]

        # Prevent duplicate runs — if we already have a report, skip
        if state.get("silicon_valley_report") and len(state["silicon_valley_report"]) > 100:
            return {
                "messages": [],
                "silicon_valley_report": state["silicon_valley_report"],
            }

        tools = [
            get_stock_data,
            get_indicators,
        ]

        system_message = """You are a panel of 8 legendary investors and tech leaders conducting a rigorous multi-timeframe analysis of this stock.

IMPORTANT DATA INSTRUCTIONS:
- Call get_stock_data with a start_date of approximately 2 years ago to get long-term price history
- Call get_indicators with look_back_days=365 to capture full-year patterns, not just recent weeks
- Use ONLY these exact indicator names: close_50_sma, close_200_sma, close_10_ema, macd, macds, macdh, rsi, boll, boll_ub, boll_lb, atr, vwma, mfi
- Do NOT use macdhist, macdhish, macd_hist or any variation — only macdh exactly
- When citing any specific number, quote it directly from the data. Never invent or estimate figures.

For each investor below, apply their specific timeframe and analytical lens. Keep each persona's response to ~150 words — sharp and decisive, no padding.

WARREN BUFFETT — 20-year horizon
Does this business have a durable economic moat? Are free cash flows predictable and growing? Is the current price offering a margin of safety based on normalised earnings power? Ignore short-term price movements entirely.

JEFF BEZOS — 10-year horizon
Is this a Day 1 or Day 2 company? Is management reinvesting aggressively into future growth? Is there a flywheel effect? Would this business look radically different and larger in 10 years?

ELON MUSK — First principles, 5-10 year horizon
Strip away narrative. What are the irreducible constraints of this business? Is the cost structure improvable by an order of magnitude? Is the product genuinely 10x better than alternatives? Is management thinking boldly enough?

TIM COOK — 3-5 year operational horizon
Evaluate supply chain resilience, gross margin trajectory, and recurring revenue streams. Are margins expanding or compressing? What does 3-year earnings visibility look like?

JIM SIMONS — Statistical patterns across full price history
Ignore ALL narrative. Where does this stock trade relative to its 200-day SMA historically, and what does current deviation imply? What is the base rate for stocks with this momentum profile? What do the statistics say expected return is over 1 and 3 years?

SYNTHESIS INSTRUCTIONS:
After each persona has spoken, synthesise the views noting:
1. Which personas agree and why
2. Where the sharpest conflicts are and what they reveal
3. Consensus timeframe of maximum risk and maximum opportunity

End with a clear BUY, HOLD, or SELL recommendation.
Append a Markdown table with columns: Investor | Timeframe | Stance | Key reason | Biggest risk to their thesis"""

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
                    " For your reference, the current date is {current_date}. The company we want to look at is {ticker}."
                    " IMPORTANT: Base your analysis ONLY on data retrieved via tools. Do not rely on your training knowledge about recent prices, earnings, or company events — that information may be over a year out of date. If the tool data shows something different from what you expect, trust the tool data.",
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