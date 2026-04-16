import os
import json
from dotenv import load_dotenv
from datetime import date

load_dotenv()

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "anthropic"
config["deep_think_llm"] = "claude-sonnet-4-6"
config["quick_think_llm"] = "claude-haiku-4-5-20251001"
config["max_debate_rounds"] = 1
config["time_horizon"] = "12_months"  # options: "1_month", "3_months", "12_months", "3_years"

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

TICKER = "VST"
RUN_DATE = date.today().strftime("%Y-%m-%d")
TIME_HORIZON = "12_months"  # options: 1_month, 3_months, 12_months, 3_years
full_state, decision = ta.propagate(TICKER, RUN_DATE, TIME_HORIZON)

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
    "time_horizon":  TIME_HORIZON,
    "verdict":       verdict,
    "full_analysis": full_state.get("final_trade_decision", decision),
    "silicon_valley_analysis": full_state.get("silicon_valley_report", ""),
    "market_analysis":         full_state.get("market_report", ""),
    "fundamentals_analysis":   full_state.get("fundamentals_report", ""),
    "investment_plan":         full_state.get("investment_plan", ""),
    "config": {
        "analysts":      ["market", "fundamentals", "silicon_valley"],
        "debate_rounds": config["max_debate_rounds"],
        "model":         config["quick_think_llm"],
        "time_horizon":  TIME_HORIZON,
    },
    "review": {
        "review_date_30d":    None,
        "review_date_90d":    None,
        "review_date_365d":   None,
        "price_at_run":       None,
        "price_at_30d":       None,
        "price_at_90d":       None,
        "price_at_365d":      None,
        "was_correct_30d":    None,
        "was_correct_90d":    None,
        "was_correct_365d":   None,
        "minimum_hold":       TIME_HORIZON,
        "notes":              None,
    }
}

log.append(record)

with open(LOG_FILE, "w") as f:
    json.dump(log, f, indent=2)

print(f"\n✓ Recommendation saved to {LOG_FILE}")
print(f"  Ticker: {TICKER} | Date: {RUN_DATE} | Verdict: {verdict}")