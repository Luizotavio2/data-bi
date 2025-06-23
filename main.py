import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Dados
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
taxa_inaptos = total_inaptos / (total_inaptos + total_aptos) * 100

# Layout
st.title("📊 Painel BI - Estudos Clínicos")

col1, col2, col3 = st.columns(3)
col1.metric("Total Aptos", total_aptos)
col2.metric("Total Inaptos", total_inaptos)
col3.metric("Taxa de Inaptos", f"{taxa_inaptos:.1f}%")

# Gráfico de barras
st.subheader("Aptos x Inaptos por Estudo")
fig1, ax1 = plt.subplots()
df_plot = df.set_index("Estudo")[["Aptos", "Inaptos"]]
df_plot.plot(kind="bar", ax=ax1, color=["#4CAF50", "black"])
plt.ylabel("Quantidade")
plt.xticks(rotation=45)
st.pyplot(fig1)

# Gráfico de pizza
st.subheader("Distribuição dos Inaptos por Estudo")
inaptos = df[df["Inaptos"] > 0].set_index("Estudo")["Inaptos"]
fig2, ax2 = plt.subplots()
ax2.pie(inaptos, labels=inaptos.index, autopct="%1.1f%%", startangle=140)
ax2.axis("equal")
st.pyplot(fig2)
