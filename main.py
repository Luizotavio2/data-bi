import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# =============================
# CONFIGURAÇÃO DE PÁGINA
# =============================
st.set_page_config(page_title="Painel de Estudos Clínicos", layout="wide")


try:
    logo = Image.open("logo-synvia.png")
    st.image(logo, width=180)
except:
    st.warning("⚠️ Logo não encontrada.")


# =============================
# TÍTULO
# =============================
st.markdown("## 📊 Painel de Captação de Participantes")
st.markdown("Análise geral dos estudos clínicos | Atualizado em 2025-06-23")
st.markdown("---")

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
    "Inaptos_Homens":   [0, 1, 0, 1, 0, 1],
    "Inaptos_Mulheres": [1, 1, 0, 0, 0, 0],
    "Aptos_Homens":     [2, 1, 0, 0, 3, 8],
    "Aptos_Mulheres":   [2, 2, 1, 1, 6, 6]
}

df = pd.DataFrame(dados)

# =============================
# CÁLCULOS
# =============================
df["Inaptos_Total"] = df["Inaptos_Homens"] + df["Inaptos_Mulheres"]
df["Aptos_Total"] = df["Aptos_Homens"] + df["Aptos_Mulheres"]
df["Total_Geral"] = df["Aptos_Total"] + df["Inaptos_Total"]

total_aptos = df["Aptos_Total"].sum()
total_inaptos = df["Inaptos_Total"].sum()
total_geral = df["Total_Geral"].sum()
taxa_inaptos = (total_inaptos / total_geral) * 100

# Comparecimentos
total_agendados = 151
total_faltaram = 114
total_compareceram = total_agendados - total_faltaram
taxa_comparecimento = (total_compareceram / total_agendados) * 100

# =============================
# KPIs
# =============================
st.markdown("### 📈 Indicadores Gerais")
col1, col2, col3, col4 = st.columns(4)
col1.metric("✅ Aptos", total_aptos)
col2.metric("❌ Inaptos", total_inaptos)
col3.metric("🧮 Total", total_geral)
col4.metric("📉 Taxa de Inaptos", f"{taxa_inaptos:.1f}%")

col5, col6 = st.columns(2)
col5.metric("📌 Agendados", total_agendados)
col6.metric("👥 Comparecimento", f"{taxa_comparecimento:.1f}%")

st.markdown("---")

# =============================
# GRÁFICO DE BARRAS
# =============================
st.subheader("📊 Distribuição por Estudo")
df_bar = df.set_index("Estudo")[["Aptos_Homens", "Aptos_Mulheres", "Inaptos_Homens", "Inaptos_Mulheres", "Total_Geral"]]
fig_bar, ax_bar = plt.subplots(figsize=(13, 5))
cores = ["#2196F3", "#9C27B0", "#0D47A1", "#BA68C8", "#424242"]

df_bar.plot(kind="bar", ax=ax_bar, color=cores)
for container in ax_bar.containers:
    ax_bar.bar_label(container, fontsize=8, padding=2)

ax_bar.set_ylabel("Quantidade")
ax_bar.set_title("📊 Distribuição por Sexo e Estudo")
ax_bar.legend(loc="upper right")
plt.xticks(rotation=30)
st.pyplot(fig_bar)


# =============================
# GRÁFICO DE PIZZA - INAPTOS
# =============================
st.markdown("### 🧩 Inaptos por Estudo (%)")
col_pie1, col_pie2 = st.columns(2)

with col_pie1:
    inaptos = df[df["Inaptos_Total"] > 0].set_index("Estudo")["Inaptos_Total"]
    fig_pie, ax_pie = plt.subplots(figsize=(4, 4))
    ax_pie.pie(
        inaptos,
        labels=inaptos.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=plt.cm.Greys(range(100, 256, int(155 / len(inaptos))))
    )
    ax_pie.axis("equal")
    st.pyplot(fig_pie)

# =============================
# GRÁFICO DE PIZZA - COMPARECIMENTO
# =============================
with col_pie2:
    st.markdown("🚷 **Faltas x Comparecimentos**")
    fig2, ax2 = plt.subplots(figsize=(4, 4))
    ax2.pie(
        [total_compareceram, total_faltaram],
        labels=["Compareceram", "Não Compareceram"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#4CAF50", "#F44336"]
    )
    ax2.axis("equal")
    st.pyplot(fig2)

# =============================
# TABELA FINAL
# =============================
st.markdown("### 📋 Tabela Resumo por Estudo")
df_final = df.copy()
df_final["% Participação"] = (df_final["Total_Geral"] / total_geral * 100).round(1)
st.dataframe(
    df_final[["Estudo", "Aptos_Total", "Inaptos_Total", "Total_Geral", "% Participação"]],
    use_container_width=True
)
