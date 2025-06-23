import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# CONFIGURAÇÃO DE PÁGINA
# =============================
st.set_page_config(layout="wide", page_title="Painel de Estudos Clínicos")

# =============================
# DADOS
# =============================
dados = {
    "Estudo": [
        "BANCO DE DADOS",
        "AZILSARTANA MEDOXOMILA",
        "BREXPIPRAZOL",
        "CLORIDRATO DE PAZOPANIBE",
        "DIPIRONA MONOIDRATADA",
        "PREGABALINA"
    ],
    "Inaptos": [1, 2, 0, 1, 0, 14],
    "Aptos":   [4, 3, 1, 1, 9, 1]
}
df = pd.DataFrame(dados)

# KPIs
total_inaptos = df["Inaptos"].sum()
total_aptos = df["Aptos"].sum()
total = total_inaptos + total_aptos
taxa_inaptos = (total_inaptos / total) * 100


# =============================
# TÍTULO
# =============================
st.markdown("## 📊 Painel Geral de Estudos Clínicos")
st.markdown("---")

# =============================
# KPIs - MÉTRICAS SUPERIORES
# =============================
col1, col2, col3 = st.columns(3)
col1.metric("✅ Total de Aptos", total_aptos)
col2.metric("❌ Total de Inaptos", total_inaptos)
col3.metric("📉 Taxa de Inaptos", f"{taxa_inaptos:.1f}%")


st.markdown("---")

# =============================
# LAYOUT COM GRÁFICOS
# =============================
col_esq, col_dir = st.columns([2, 1])

# GRÁFICO DE BARRAS
with col_esq:
    st.subheader("📚 Distribuição de Aptos e Inaptos por Estudo")
    fig_bar, ax_bar = plt.subplots(figsize=(10, 4))
    df.set_index("Estudo")[["Aptos", "Inaptos"]].plot(kind="bar", ax=ax_bar, color=["#4CAF50", "black"])
    ax_bar.set_ylabel("Quantidade")
    ax_bar.set_title("Comparativo por Estudo")
    plt.xticks(rotation=30)
    st.pyplot(fig_bar)


with col_dir:
    st.subheader("🧩 Inaptos por Estudo (%)")
    inaptos = df[df["Inaptos"] > 0].set_index("Estudo")["Inaptos"]
    fig_pie, ax_pie = plt.subplots(figsize=(4, 4))
    ax_pie.pie(inaptos, labels=inaptos.index, autopct="%1.1f%%", startangle=140, colors=["black", "#444", "#777", "#999"])
    ax_pie.axis("equal")
    st.pyplot(fig_pie)

st.markdown("### 📋 Tabela Detalhada")
st.dataframe(df.style.highlight_max(axis=0, color='lightgreen'), use_container_width=True)
