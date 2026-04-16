import time
import json

def create_research_manager(llm, memory):
    def research_manager_node(state) -> dict:
        history = state["investment_debate_state"].get("history", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]
        investment_debate_state = state["investment_debate_state"]
        time_horizon = state.get("time_horizon", "12_months")

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)
        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        horizon_guidance = {
            "1_month":   "Focus on technical momentum, near-term catalysts, and sentiment. Valuation matters less. Short-term price action is signal not noise.",
            "3_months":  "Balance momentum and fundamentals. Upcoming earnings, guidance, and macro catalysts are key drivers.",
            "12_months": "Fundamentals and competitive position dominate. Short-term volatility is irrelevant. Weight earnings power and moat quality.",
            "3_years":   "Moat durability, management quality, and TAM expansion dominate. Current valuation only matters as margin of safety.",
        }.get(time_horizon, "Fundamentals and competitive position dominate.")

        current_date = state.get("trade_date", "unknown")

        prompt = f"""You are the portfolio manager and debate facilitator making a {time_horizon} investment recommendation.

TODAY'S DATE: {current_date}. All analysis below reflects data as of this date. Do not reference events, prices, or earnings from before this date as if they are upcoming — they may already be history. Base your conclusions solely on the reports provided.

TIME HORIZON: {time_horizon}
GUIDANCE: {horizon_guidance}
Calibrate the weight you give to short-term vs long-term factors accordingly. A risk that matters for a 1_month call may be completely irrelevant for a 3_years call and vice versa.

CALIBRATION RULES — apply these before reaching a conclusion:
1. Base rate: Equities rise roughly 70% of years. SELL requires specific evidence of overvaluation or fundamental deterioration — not just the presence of risks, which always exist.
2. HOLD is only valid when: the bull and bear cases are genuinely balanced AND there is a specific near-term catalyst or data point that would resolve the uncertainty. Do not use HOLD as a default when uncertain.
3. Already-priced risks: If the bear's concerns are widely known and already reflected in a depressed valuation, they do not justify SELL. The question is always whether risks are WORSE than what the market has priced.
4. Distinguish temporary from permanent: Cyclical headwinds, macro uncertainty, and short-term earnings misses are not structural impairments. Weight them accordingly.
5. Avoid loss-aversion bias: The pain of a loss feels larger than an equivalent gain, which causes systematic under-buying of quality assets at depressed prices. Correct for this explicitly.
6. HOLD checklist: Before writing HOLD, answer — what specific event in the next 60 days resolves the uncertainty? If that event goes well, would you say BUY? If yes and probability is above 50%, BUY now is better than HOLD and wait.

Your output must include:
- Time horizon: Restate the horizon you are deciding for
- Your Recommendation: BUY, SELL, or HOLD with a decisive stance
- Rationale: The specific arguments that drove your conclusion, and why they outweighed the opposing case
- What would change your mind: One or two specific data points that would flip your recommendation
- Strategic Actions: Concrete steps for implementing the recommendation including position sizing and time horizon
- Past lessons applied: How you are incorporating past mistakes into this decision

Present your analysis conversationally without special formatting.

Past reflections on mistakes:
\"{past_memory_str}\"

Debate History:
{history}"""

        response = llm.invoke(prompt)
        new_investment_debate_state = {
            "judge_decision": response.content,
            "history": investment_debate_state.get("history", ""),
            "bear_history": investment_debate_state.get("bear_history", ""),
            "bull_history": investment_debate_state.get("bull_history", ""),
            "current_response": response.content,
            "count": investment_debate_state["count"],
        }
        return {
            "investment_debate_state": new_investment_debate_state,
            "investment_plan": response.content,
            "trader_investment_plan": response.content,
        }
    return research_manager_node