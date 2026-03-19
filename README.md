# 🤖 TradingAgents — Silicon Valley Fork

> ⚠️ For research purposes only. Not financial advice.

[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](https://sanaships.github.io/TradingAgents)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-Apache_2.0-gray)](LICENSE)

A fork of [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) extended with a custom **Silicon Valley Panel analyst** — 8 legendary investors who debate each other before reaching a final recommendation.

---

## ✦ What's different in this fork

The original framework includes market, news, fundamentals, and sentiment analysts feeding into a bull/bear debate and risk management team. This fork adds a custom **Silicon Valley Panel** that sits alongside those agents.

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

## 📋 Example output — Vertiv Holdings (VRT)

> Full analysis run on March 19, 2026

**📉 Market analyst**
VRT up 85% in 6 months, currently $264. Golden cross confirmed (50 SMA above 200 SMA). However MACD declining from peak of 19.4 to 13.3 while price made new highs — classic negative divergence. RSI at 62, ATR elevated at $13.55. Likely entering consolidation. Support at $245–250.

**📰 News analyst**
Expanded NVIDIA collaboration on Vera Rubin DSX AI factory infrastructure. New BYOP&C partnership with Generate Capital addresses grid-constrained markets. CEO confirmed liquid cooling capacity growing "really, really rapidly." Wall Street analysts say stock "not done" despite 50% YTD gain.

**📊 Fundamentals analyst**
Revenue $2.88B in Q4 2025, up 22.7% YoY. Net income grew 202% YoY to $445M. Gross margins expanded 520bps to 38.9%. Free cash flow $884M at 30.7% margin. Net debt declining — now 0.54x EBITDA. Forward P/E 33x implies 134% earnings growth expected. Execution risk is real at these multiples.

**✦ Silicon Valley panel**

| Investor | Stance | Key reason |
|---|---|---|
| 🏦 Buffett | SELL | 78x trailing P/E unjustifiable for cyclical business |
| 📦 Bezos | CAUTIOUS | Momentum deceleration signals Day 2 fatigue |
| 🚀 Musk | SELL | Priced for perfection, momentum crowded |
| 🍎 Cook | HOLD | Margin sustainability unproven at scale |
| 🔍 Pichai | CAUTIOUS BULL | NVIDIA partnership real, platform not yet monetised |
| 📈 Gurley | SELL | Margin compression inevitable as Modine/Schneider scale |
| ⚡ Huang | HOLD | Right trend, wrong price — wait for $200–220 |
| 📊 Simons | SELL | MACD divergence + volume fadeout = reversal imminent |

**Consensus:** 5 of 8 bearish or cautious. Fair value range $200–$250 vs current $265.

**🐂 Bull researcher**
NVIDIA partnership and BYOP&C alliance are structural moat-builders. Liquid cooling is a 10-year secular trend. Management executing ahead of competitors on capacity.

**🐻 Bear researcher**
Valuation prices in perfection. Modine achieving 95% of Vertiv's performance creates real margin compression risk. Q4 FCF inflated by $480M working capital release unlikely to repeat.

**⚖️ Risk verdict**

> **FINAL TRANSACTION PROPOSAL: HOLD**
>
> If you own it — hold with stop at $230, consider trimming 30–40% at current levels.
> If you don't own it — wait for pullback to $220–238 before initiating.
> Re-evaluate on: Q1 2026 earnings, NVIDIA Rubin deployment timeline, any Modine pricing moves.

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
