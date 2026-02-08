import streamlit as st, tempfile, os

from portfolio_data import portfolio_data
from news_loader import load_news
from prompt_builder import build_prompt
from ai_client import get_ai_client
from ai_analysis import run_ai, extract_json_safe
from dataframes import fund_df, summary_df, rebalance_df, news_df
from charts import allocation_pie, risk_return, rebalance_bar, risk_gauge

st.title("Advisor Copilot")

# Client selection
clients = portfolio_data["clients"]
idx = st.selectbox("Select Client",
                   range(len(clients)),
                   format_func=lambda i: f"{clients[i]['name']} ({clients[i]['riskProfile']})")
client = clients[idx]

# News upload
file = st.file_uploader("Upload news", type=["txt", "pdf", "docx"])

suffix = os.path.splitext(file.name)[1]

if file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.read())
        path = tmp.name

    news_text = load_news(path)
    os.remove(path)

    if st.button("Run Analysis"):
        ai = get_ai_client()
        prompt = build_prompt(portfolio_data, client, news_text)

        raw = run_ai(prompt, ai)
        ai_data = extract_json_safe(raw)

        if not ai_data:
            st.error("Invalid AI output")
            st.stop()

        df_f = fund_df(ai_data)
        df_s = summary_df(ai_data)
        df_r = rebalance_df(ai_data)
        df_n = news_df(ai_data)
        summary = ai_data.get("portfolioSummary", {})

        st.dataframe(df_f)
        st.dataframe(df_s)
        st.dataframe(df_r)
        st.dataframe(df_n)

        if allocation_pie(summary):
            st.plotly_chart(allocation_pie(summary), use_container_width=True)
        if risk_return(df_f):
            st.plotly_chart(risk_return(df_f), use_container_width=True)
        if rebalance_bar(df_r):
            st.plotly_chart(rebalance_bar(df_r), use_container_width=True)

        st.plotly_chart(risk_gauge(summary.get("overallRiskScore")))
