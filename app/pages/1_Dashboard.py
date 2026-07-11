"""Pagina de dashboard: metricas de uso e feedback armazenados no Postgres."""

import plotly.express as px
import streamlit as st

from app.utils.db import fetch_interactions

st.set_page_config(page_title="Dashboard RAG", page_icon=":bar_chart:", layout="wide")
st.title("Dashboard de Monitoramento")

df = fetch_interactions()

if df.empty:
    st.info("Ainda nao ha interacoes registradas.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de interacoes", len(df))
col2.metric("Latencia media (ms)", f"{df['latency_ms'].mean():.0f}")
col3.metric("Tokens medios/resposta", f"{df['total_tokens'].mean():.0f}")

rated = df["rating"].notna().sum()
positive_rate = (df["rating"] == 1).sum() / rated if rated else 0
col4.metric("Taxa de feedback positivo", f"{positive_rate:.0%}")

st.subheader("Interacoes ao longo do tempo")
timeline = df.set_index("created_at").resample("D").size().reset_index(name="interacoes")
st.plotly_chart(px.line(timeline, x="created_at", y="interacoes"), use_container_width=True)

st.subheader("Distribuicao de latencia")
st.plotly_chart(px.histogram(df, x="latency_ms", nbins=30), use_container_width=True)

st.subheader("Ultimas interacoes com feedback")
st.dataframe(
    df[["created_at", "question", "answer", "rating", "feedback_comment"]].head(50),
    use_container_width=True,
)
