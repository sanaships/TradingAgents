# 🤖 TradingAgents — Silicon Valley Fork

> ⚠️ For research purposes only. Not financial advice.

[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-Apache_2.0-gray)](LICENSE)

A fork of [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) with a custom **Silicon Valley Panel analyst** and a significantly refactored pipeline. Agents debate a stock from opposing frameworks, then a Risk Judge delivers a calibrated final recommendation with position sizing.

---

## ✦ What's different in this fork

### Custom Silicon Valley Panel
Rather than a single analyst perspective, five legendary investor personas each evaluate the stock through a distinct lens — then debate each other. The tension between opposing frameworks surfaces blind spots that a single analyst misses.

| Investor | Lens |
|---|---|
| 🏦 Warren Buffett | Durable moat, 20-year hold test, free cash flow |
| 📦 Jeff Bezos | Day 1 vs Day 2, flywheel compounding |
| 🚀 Elon Musk | First principles — is the physics of the business sound? |
| 🍎 Tim Cook | Supply chain, margins, recurring revenue visibility |
| 📊 Jim Simons | Ignore the narrative — what do the patterns say statistically? |

### Pipeline improvements vs. upstream
- **Removed the Trader node** — redundant with Research Manager; saves one LLM call per run
- **Risk debate agents trimmed** — Aggressive/Conservative/Neutral now receive only the investment plan, not all four raw reports (significant token reduction with no quality loss)
- **Bug fix: trade date never reached agents** — upstream code passed `time_horizon` as `trade_date`, so every agent saw `"12_months"` as today's date
- **Date-grounding prompts** — all analysts instructed to rely only on tool-fetched data, not training knowledge (model cutoff is mid-2025)
- **ADR currency warnings** — fundamentals analyst flags when price (USD) and financial statements (local currency) are mismatched for foreign ADRs
- **Show-your-math** — fundamentals analyst required to show formula + source numbers for every computed ratio
- **Verdict extraction fix** — uses last whole-word match, so "not a BUY, it's a HOLD" correctly returns HOLD
- **Auto-retry on Anthropic 529 overload** — `max_retries=5` baked into the LLM client
- **Full debug visibility** — all nodes (Bull/Bear/Research Manager/Risk Judge) now print output during debug runs

---

## 🏗️ Architecture

```
Analyst team (sequential)
├── 📉 Market analyst       (RSI, MACD, SMA, Bollinger Bands, price action)
├── 📊 Fundamentals analyst (balance sheet, cash flow, income statement)
└── ✦  Silicon Valley panel (5 investor personas, ~150 words each) ← custom

Research team
├── 🐂 Bull researcher
└── 🐻 Bear researcher
      ↓
💼 Research Manager  (BUY / HOLD / SELL + investment plan)
      ↓
⚖️  Risk debate
├── 🔴 Aggressive analyst
├── 🟢 Conservative analyst
└── 🟡 Neutral analyst
      ↓
🏛️  Risk Judge → final recommendation + position sizing
```

---

## 📋 Example — Vistra Corp (VST), April 16 2026

**Verdict: HOLD** ✓ — VST declined ~2.7% over the following two weeks, validating the cautious stance.

**What the pipeline saw:**
- Price $165.53, sitting 9% below 200-SMA — already in correction
- MACD histogram improving (-3.67 → -0.31), RSI neutral at 56
- EBITDA margin compressed ~1,200bps YoY on only 2.9% revenue growth
- $4.2B current debt due for refinancing; capex running at $2.75B/yr

**Silicon Valley panel:** Unanimous HOLD — AI/data center power demand thesis real but EBITDA trajectory unresolved. Simons: RSI in neutral bounce zone, no confirmation signal.

**Research Manager reasoning:**
> *"The bear landed several hits I cannot dismiss. The EBITDA margin compression of nearly 1,200 basis points in a single year, against only 2.9% revenue growth, is not explained away by calling it cyclical without showing the mechanism. The $4.2 billion in current debt represents a real near-term refinancing event.*
>
> *But many of these risks are visible and widely discussed — meaning they're at least partially priced into a stock already sitting 16% below its 200-day moving average."*
>
> **HOLD. Flip trigger: next quarterly report shows EBITDA stabilisation.**

**Risk Judge:** Confirmed HOLD. Position sizing: 0% new money until EBITDA margin stabilises; existing holders maintain with stop below 200-SMA.

---

## 🚀 Quickstart

```bash
# 1. Clone
git clone https://github.com/sanaships/TradingAgents
cd TradingAgents

# 2. Set up environment (Python 3.11 required)
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Add API key
cp .env.example .env
# Add ANTHROPIC_API_KEY to .env

# 4. Configure run.py — set TICKER, TIME_HORIZON, selected analysts

# 5. Run
python3 run.py
```

### Configuration

```python
config["deep_think_llm"]          = "claude-sonnet-4-6"        # Research Manager + Risk Judge
config["quick_think_llm"]         = "claude-haiku-4-5-20251001" # All other agents
config["max_debate_rounds"]       = 1   # Bull/Bear rounds
config["max_risk_discuss_rounds"] = 1   # Risk debate rounds

TIME_HORIZON = "12_months"  # 1_month | 3_months | 12_months | 3_years
```

### Note on foreign ADRs
For foreign companies traded as US ADRs (e.g. TSM, BABA, ASML), yfinance may return financial statements in local currency while price data is in USD. The fundamentals analyst will flag this mismatch. For reliable valuation ratios, use the local ticker (e.g. `2330.TW` for TSMC) or treat computed ratios as indicative only.

---

## 📄 Citation

Built on top of [TradingAgents](https://github.com/TauricResearch/TradingAgents) by Tauric Research.

```
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
  title={TradingAgents: Multi-Agents LLM Financial Trading Framework},
  author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
  year={2025},
  eprint={2412.20138},
  url={https://arxiv.org/abs/2412.20138}
}
```
