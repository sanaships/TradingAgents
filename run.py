import os
import json
from dotenv import load_dotenv
from datetime import date

load_dotenv()

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "anthropic"
config["deep_think_llm"] = "claude-haiku-4-5-20251001"
config["quick_think_llm"] = "claude-haiku-4-5-20251001"
config["max_debate_rounds"] = 1

ta = TradingAgentsGraph(
    selected_analysts=[
        "market",
        # "social",
        # "news",
        "fundamentals",
        "silicon_valley",
    ],
    debug=True,
    config=config
)

TICKER = "FXI"
RUN_DATE = date.today().strftime("%Y-%m-%d")

_, decision = ta.propagate(TICKER, RUN_DATE)
print(decision)

# ── Save structured recommendation log ────────────────────────
LOG_FILE = "recommendations_log.json"

# Load existing log or start fresh
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        log = json.load(f)
else:
    log = []

# Parse the decision for a clean verdict
verdict = "UNKNOWN"
for word in ["BUY", "HOLD", "SELL"]:
    if word in decision.upper():
        verdict = word
        break

# Build the record
record = {
    "ticker":        TICKER,
    "run_date":      RUN_DATE,
    "verdict":       verdict,
    "full_analysis": decision,
    "config": {
        "analysts":      ["market", "fundamentals", "silicon_valley"],
        "debate_rounds": config["max_debate_rounds"],
        "model":         config["quick_think_llm"],
    },
    "review": {
        "review_date":     None,
        "price_at_run":    None,
        "price_at_review": None,
        "actual_outcome":  None,
        "was_correct":     None,
        "notes":           None,
    }
}

log.append(record)

with open(LOG_FILE, "w") as f:
    json.dump(log, f, indent=2)

print(f"\n✓ Recommendation saved to {LOG_FILE}")
print(f"  Ticker: {TICKER} | Date: {RUN_DATE} | Verdict: {verdict}")