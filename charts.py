import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def allocation_pie(summary):
    alloc = summary.get("assetAllocation", {})
    if not alloc: return None
    df = pd.DataFrame({"Asset": alloc.keys(), "Allocation": alloc.values()})
    return px.pie(df, names="Asset", values="Allocation")

def risk_return(df):
    if df.empty: return None
    return px.scatter(df, x="volatility", y="return1Y",
                      size="currentAllocation", color="riskLevel",
                      hover_name="fund")

def rebalance_bar(df):
    if df.empty: return None
    return px.bar(df, x="fund", y="allocationChangePercent", color="action")

def risk_gauge(score):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=score or 0,
        gauge={"axis": {"range": [0, 10]}}
    ))
