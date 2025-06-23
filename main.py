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
<<<<<<< HEAD
    "Inaptos_Homens":   [0, 1, 0, 1, 0, 1],
    "Inaptos_Mulheres": [1, 1, 0, 0, 0, 0],
    "Aptos_Homens":     [2, 1, 0, 0, 3, 8],
    "Aptos_Mulheres":   [2, 2, 1, 1, 6, 6]
=======
    "Inaptos": [1, 2, 0, 1, 0, 1],
    "Aptos":   [4, 3, 1, 1, 9, 14]
>>>>>>> 4b265f629403d09de20bc8e7928cfc17f6a975ee
}

df = pd.DataFrame(dados)

# =============================
# CÁLCULOS DE TOTAIS
# =============================
df["Inaptos_Total"] = df["Inaptos_Homens"] + df["Inaptos_Mulheres"]
df["Aptos_Total"] = df["Aptos_Homens"] + df["Aptos_Mulheres"]
df["Total_Geral"] = df["Aptos_Total"] + df["Inaptos_Total"]

# =============================
# KPIs - GLOBAIS
# =============================
total_aptos = df["Aptos_Total"].sum()
total_inaptos = df["Inaptos_Total"].sum()
total = df["Total_Geral"].sum()
taxa_inaptos = (total_inaptos / total) * 100

# =============================
# TÍTULO
# =============================
st.markdown("## 📊 Painel Geral de Estudos Clínicos por Gênero")
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
    st.subheader("📚 Aptos e Inaptos por Gênero e Estudo (com Totais)")
    df_bar = df.set_index("Estudo")[[
        "Aptos_Homens", "Aptos_Mulheres", "Inaptos_Homens", "Inaptos_Mulheres", "Total_Geral"
    ]]
    fig_bar, ax_bar = plt.subplots(figsize=(13, 5))
    df_bar.plot(
        kind="bar",
        ax=ax_bar,
        color=[
            "#2196F3",  # azul - homens aptos
            "#9C27B0",  # roxo - mulheres aptas
            "#0D47A1",  # azul escuro - homens inaptos
            "#BA68C8",  # roxo claro - mulheres inaptas
            "#424242"   # cinza escuro - total geral
        ]
    )
    ax_bar.set_ylabel("Quantidade")
    ax_bar.set_title("Distribuição por Estudo, Sexo e Total")
    ax_bar.legend([
        "Aptos (Homens)", "Aptos (Mulheres)",
        "Inaptos (Homens)", "Inaptos (Mulheres)",
        "Total Geral"
    ])
    plt.xticks(rotation=30)
    st.pyplot(fig_bar)

# GRÁFICOS DE PIZZA
with col_dir:
    # Gráfico de Pizza - Inaptos
    st.subheader("🧩 Inaptos por Estudo (%)")
    inaptos = df[df["Inaptos_Total"] > 0].set_index("Estudo")["Inaptos_Total"]
    fig_pie, ax_pie = plt.subplots(figsize=(4, 4))
    ax_pie.pie(inaptos, labels=inaptos.index, autopct="%1.1f%%", startangle=140,
               colors=["#444", "#777", "#999", "#bbb", "#222", "#888"])
    ax_pie.axis("equal")
    st.pyplot(fig_pie)

    st.markdown("---")

    # Gráfico de Pizza - Agendados que Não Compareceram (Total Geral)
    st.subheader("🚫 Não comparecimentos")

    # Ajuste os valores conforme seu dado real
    total_agendados = 151
    total_faltaram = 114  # Altere este valor para o seu número real

    # Controle para evitar erro com valores negativos
    total_faltaram = min(total_faltaram, total_agendados)
    total_compareceram = total_agendados - total_faltaram

    labels = ["Compareceram", "Não Compareceram"]
    sizes = [total_compareceram, total_faltaram]
    colors = ["#4CAF50", "#F44336"]

    fig2, ax2 = plt.subplots(figsize=(4, 4))
    ax2.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
    ax2.axis("equal")
    st.pyplot(fig2)

# =============================
# TABELA DETALHADA SIMPLIFICADA
# =============================
st.markdown("### 📋 Tabela Detalhada por Sexo e Totais")
st.dataframe(
    df[["Estudo", "Aptos_Total", "Inaptos_Total", "Total_Geral"]],
    use_container_width=True
)
