import os
from dotenv import load_dotenv
load_dotenv()

from datetime import date
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "anthropic"
config["deep_think_llm"] = "claude-haiku-4-5-20251001"
config["quick_think_llm"] = "claude-haiku-4-5-20251001"
config["max_debate_rounds"] = 2

ta = TradingAgentsGraph(
    selected_analysts=[
    "market",
# "social", 
# "news", 
    "fundamentals", 
    "silicon_valley"],
    debug=True,
    config=config
)

_, decision = ta.propagate("ANET", date.today().strftime("%Y-%m-%d"))
print(decision)