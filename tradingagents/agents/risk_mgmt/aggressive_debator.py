import time
import json

def create_aggressive_debator(llm):
    def aggressive_node(state) -> dict:
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        aggressive_history = risk_debate_state.get("aggressive_history", "")
        current_conservative_response = risk_debate_state.get("current_conservative_response", "")
        current_neutral_response = risk_debate_state.get("current_neutral_response", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]
        trader_decision = state["trader_investment_plan"]
        company = state["company_of_interest"]

        prompt = f"""As the Aggressive Risk Analyst, your role is to actively champion high-reward opportunities, emphasizing bold strategies and competitive advantages. When evaluating the trader's decision or plan, focus on the potential upside, growth potential, and innovative benefits — even when these come with elevated risk.

Use the provided market data and sentiment analysis to strengthen your arguments and challenge opposing views. Respond directly to each point made by the conservative and neutral analysts, countering with data-driven rebuttals and persuasive reasoning. Highlight where their caution might miss critical opportunities or where their assumptions are overly conservative.

Here is the trader's decision:
{trader_decision}

Your task is to create a compelling case by questioning and critiquing the conservative and neutral stances to demonstrate why your high-reward perspective offers the best path forward. Incorporate insights from:

Market Research Report: {market_research_report}
Social Media Sentiment Report: {sentiment_report}
Latest World Affairs Report: {news_report}
Company Fundamentals Report: {fundamentals_report}
Current conversation history: {history}
Last conservative analyst argument: {current_conservative_response}
Last neutral analyst argument: {current_neutral_response}

If there are no responses from the other viewpoints, do not hallucinate — just present your point.

Engage actively by addressing specific concerns raised, refuting weaknesses in their logic, and asserting the benefits of calculated risk-taking. Challenge each counterpoint to underscore why a high-reward approach is optimal.

ALTERNATIVE OPPORTUNITIES:
After making your case, end with a section called "High-Conviction Alternatives" where you identify 2-3 alternative stocks or ETFs worth considering alongside or instead of {company}. For each alternative:
- Name the ticker and company
- Explain in one sentence why it has superior risk/reward compared to {company} right now
- Categorize it as: HIGHER RISK/HIGHER REWARD, SIMILAR RISK/BETTER REWARD, or LOWER RISK/SIMILAR REWARD
- Note the key catalyst or thesis in one sentence

Base your alternatives on the same sector, macro theme, or investment thesis as {company}. If the trader's plan is bearish on {company}, suggest what to rotate into instead. If bullish, suggest complementary positions that amplify the same thesis.

Output conversationally as if you are speaking, without any special formatting except for the High-Conviction Alternatives section at the end."""

        response = llm.invoke(prompt)
        argument = f"Aggressive Analyst: {response.content}"
        new_risk_debate_state = {
            "history": history + "\n" + argument,
            "aggressive_history": aggressive_history + "\n" + argument,
            "conservative_history": risk_debate_state.get("conservative_history", ""),
            "neutral_history": risk_debate_state.get("neutral_history", ""),
            "latest_speaker": "Aggressive",
            "current_aggressive_response": argument,
            "current_conservative_response": risk_debate_state.get("current_conservative_response", ""),
            "current_neutral_response": risk_debate_state.get("current_neutral_response", ""),
            "count": risk_debate_state["count"] + 1,
        }
        return {"risk_debate_state": new_risk_debate_state}
    return aggressive_node