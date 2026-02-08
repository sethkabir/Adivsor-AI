import pandas as pd

def fund_df(ai): return pd.DataFrame(ai.get("fundAnalytics", []))
def summary_df(ai):
    s = ai.get("portfolioSummary", {})
    return pd.DataFrame({
        "Metric": ["Risk", "Return %", "Diversification"],
        "Value": [s.get("overallRiskScore"), s.get("expectedReturn"), s.get("diversificationScore")]
    })
def rebalance_df(ai): return pd.DataFrame(ai.get("rebalancingActions", []))
def news_df(ai): return pd.DataFrame(ai.get("newsImpactAnalysis", []))
