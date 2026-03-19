# 🤖 TradingAgents — Silicon Valley Fork

> ⚠️ For research purposes only. Not financial advice.

[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](https://sanaships.github.io/TradingAgents)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-Apache_2.0-gray)](LICENSE)

A fork of [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) extended with a custom **Silicon Valley Panel analyst** — 8 legendary investors who debate each other before reaching a final recommendation.

---

## ✦ What's different in this fork

The original framework includes market, news, sentiment, and fundamentals analysts feeding into a bull/bear debate and risk management team. This fork adds a custom **Silicon Valley Panel** that sits alongside those agents.

Rather than a single perspective, 8 investor personas each evaluate the stock from their unique lens — then debate each other. The tension between opposing frameworks produces more nuanced output than any single analyst.

| Investor | Lens |
|---|---|
| 🏦 Warren Buffett | Durable moat, 20-year hold test, predictable FCF |
| 📦 Jeff Bezos | Day 1 vs Day 2, long-term compounding, customer obsession |
| 🚀 Elon Musk | First principles — is the physics of the business sound? |
| 🍎 Tim Cook | Supply chain, margins, services attach rate |
| 🔍 Sundar Pichai | AI integration, platform potential, developer ecosystem |
| 📈 Bill Gurley | Market size, rake, margin compression risk |
| ⚡ Jensen Huang | Is AI genuinely core, or just a buzzword? |
| 📊 Jim Simons | Ignore the narrative — what do the patterns say? |

---

## 🧠 Why it produces better analysis

**8 distinct mental models, not one** — each persona has a radically different framework. Buffett's moat thinking directly challenges Musk's first-principles skepticism. Simons ignores both and looks at pure patterns.

**⚡ Adversarial debate** — that tension surfaces blind spots a single analyst misses.

**🎯 Nuanced output** — because the personas disagree, the final result includes price targets, re-evaluation triggers, and position sizing guidance, not just a binary BUY / SELL.

---

## 🏗️ Architecture
```
Analyst team
├── 📉 Market analyst       (RSI, MACD, SMA, price action)
├── 📰 News analyst         (headlines, macro, insider data)
├── 📊 Fundamentals analyst (balance sheet, cash flow, P/E)
└── ✦  Silicon Valley panel (8 investor personas) ← custom

Research team
├── 🐂 Bull researcher
└── 🐻 Bear researcher

💼 Trader agent

⚖️ Risk management
├── 🔴 Aggressive
├── 🟡 Neutral
└── 🟢 Conservative

→ Final decision: BUY / HOLD / SELL with rationale
```

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

# 4. Run
python3 run.py
```

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
