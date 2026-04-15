import time
import json

def create_risk_manager(llm, memory):
    def risk_manager_node(state) -> dict:
        company_name = state["company_of_interest"]
        history = state["risk_debate_state"]["history"]
        risk_debate_state = state["risk_debate_state"]
        market_research_report = state["market_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]
        sentiment_report = state["sentiment_report"]
        trader_plan = state["investment_plan"]
        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)
        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        prompt = f"""You are the Risk Management Judge. Your goal is to evaluate the debate between three risk analysts — Aggressive, Neutral, and Conservative — and deliver a final, calibrated recommendation: BUY, SELL, or HOLD.

CALIBRATION RULES — apply these before reaching a conclusion:
1. Your job is risk-ADJUSTED decision making, not risk elimination. Every investment has risk. The question is whether expected return compensates for the risk, not whether risk exists.
2. If all three analysts agree, you MUST steelman the opposing view before confirming the consensus. Unanimous agreement is a signal to check for groupthink, not to rubber-stamp the conclusion.
3. HOLD is only valid when there is a specific near-term catalyst or data point that would resolve genuine uncertainty. It is not a safe default.
4. SELL requires evidence that: (a) the stock is overvalued relative to fundamentals, OR (b) there is a specific catalyst for fundamental deterioration. General macro uncertainty alone does not justify SELL.
5. BUY requires evidence that: (a) risk/reward is asymmetrically positive, AND (b) the bull case is not already fully priced in.
6. Loss-aversion correction: Systematically check whether your instinct toward caution reflects genuine analysis or the psychological discomfort of recommending BUY in an uncertain environment.

Your deliverables:
- Final Recommendation: BUY, SELL, or HOLD — decisive and specific
- Risk-adjusted rationale: Why the expected return justifies or does not justify the risk at current prices
- Steelman check: The strongest argument against your conclusion, and why you are overriding it
- Refined trader plan: Start with the trader's plan ({trader_plan}) and adjust based on the risk debate
- Position sizing guidance: How much conviction warrants what size position
- Past lessons applied: Specific mistakes from past reflections being corrected in this decision

Past reflections on mistakes:
\"{past_memory_str}\"

Analysts Debate History:
{history}

Focus on actionable, calibrated decisions. The goal is accurate recommendations, not cautious ones."""

        response = llm.invoke(prompt)
        new_risk_debate_state = {
            "judge_decision": response.content,
            "history": risk_debate_state["history"],
            "aggressive_history": risk_debate_state["aggressive_history"],
            "conservative_history": risk_debate_state["conservative_history"],
            "neutral_history": risk_debate_state["neutral_history"],
            "latest_speaker": "Judge",
            "current_aggressive_response": risk_debate_state["current_aggressive_response"],
            "current_conservative_response": risk_debate_state["current_conservative_response"],
            "current_neutral_response": risk_debate_state["current_neutral_response"],
            "count": risk_debate_state["count"],
        }
        return {
            "risk_debate_state": new_risk_debate_state,
            "final_trade_decision": response.content,
        }
    return risk_manager_node
