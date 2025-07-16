import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io

st.set_page_config(page_title="Painel de Estudos Clínicos", layout="wide")


try:
    logo = Image.open("logo-synvia.png").convert("RGBA")
    largura, altura = logo.size
    fundo = Image.new("RGBA", (largura + 20, altura + 20), (255, 255, 255, 200))
    fundo.paste(logo, (10, 10), logo)
    st.image(fundo, width=180)
except:
    st.warning("⚠️ Logo não encontrada.")

st.markdown("## 📊 Painel de Captação de Participantes")
st.markdown("Análise geral dos estudos clínicos | Atualizado em 2025-07-16")
st.markdown("---")

dados = {
    "Estudo": [
        "BANCO DE DADOS",
        "BD POMADA",
        "APIXABANA",
        "CLORIDRATO DE NEBIVOLOL 2ºG",
        "CLORIDRATO DE PAZOPANIBE 3ºG",
        "PREGABALINA"
    ],
    "Inaptos_Homens":       [0, 0, 2, 0, 4, 2],
    "Inaptos_Mulheres":     [0, 0, 1, 0, 1, 5],
    "Aptos_Homens":         [2, 1, 10,0, 4, 13],
    "Aptos_Mulheres":       [2, 1, 1, 1, 3, 23],
    "Desistentes_Homens":   [0, 0, 0, 0, 1, 0],
    "Desistentes_Mulheres": [0, 1, 0, 1, 0, 0]
}

df = pd.DataFrame(dados)

df["Inaptos_Total"] = df["Inaptos_Homens"] + df["Inaptos_Mulheres"]
df["Aptos_Total"] = df["Aptos_Homens"] + df["Aptos_Mulheres"]
df["Desistentes_Total"] = df["Desistentes_Homens"] + df["Desistentes_Mulheres"]
df["Total_Geral"] = df["Aptos_Total"] + df["Inaptos_Total"] + df["Desistentes_Total"]

total_aptos = df["Aptos_Total"].sum()
total_inaptos = df["Inaptos_Total"].sum()
total_desistentes = df["Desistentes_Total"].sum()
total_geral = df["Total_Geral"].sum()
taxa_inaptos = (total_inaptos / total_geral) * 100

total_agendados = 235
total_faltaram = total_agendados - df["Total_Geral"].sum()
total_compareceram = total_agendados - total_faltaram
taxa_comparecimento = (total_compareceram / total_agendados) * 100

st.markdown("### 📈 Indicadores Gerais")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("✅ Aptos", total_aptos)
col2.metric("❌ Inaptos", total_inaptos)
col3.metric("🧮 Total", total_geral)
col4.metric("📉 Taxa de Inaptos", f"{taxa_inaptos:.1f}%")

col5, col6, col7 = st.columns(3)
col5.metric("🚫 Desistentes", f"{total_desistentes}")
col6.metric("📌 Agendados", total_agendados)
col7.metric("👥 Comparecimento", f"{taxa_comparecimento:.1f}%")

st.markdown("---")

st.subheader("📊 Distribuição por Estudo")
df_bar = df.set_index("Estudo")[["Aptos_Homens", "Aptos_Mulheres", "Inaptos_Homens", "Inaptos_Mulheres", "Desistentes_Homens", "Desistentes_Mulheres", "Total_Geral"]]
fig_bar, ax_bar = plt.subplots(figsize=(13, 5))
cores = [
    "#4CAF50",  
    "#81C784",  
    "#9C27B0",  
    "#E1BEE7",  
    "#FF7043",  
    "#FFAB91",  
    "#212121"  
]


df_bar.plot(kind="bar", ax=ax_bar, color=cores)
for container in ax_bar.containers:
    ax_bar.bar_label(container, fontsize=8, padding=2)

ax_bar.set_ylabel("Quantidade")
ax_bar.set_title("📊 Distribuição por Sexo e Estudo")
ax_bar.legend(loc="upper right")
plt.xticks(rotation=30)
st.pyplot(fig_bar)


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

st.markdown("### 📋 Tabela Resumo por Estudo")
df_final = df.copy()
df_final["% Participação"] = (df_final["Total_Geral"] / total_geral * 100).round(1)
st.dataframe(
    df_final[["Estudo", "Aptos_Total", "Inaptos_Total", "Total_Geral", "% Participação"]],
    use_container_width=True
)

img_buffer_bar = io.BytesIO()
fig_bar.savefig(img_buffer_bar, format='png', dpi=300, bbox_inches='tight')
img_buffer_bar.seek(0)

img_buffer_pie = io.BytesIO()
fig_pie.savefig(img_buffer_pie, format='png', dpi=300, bbox_inches='tight')
img_buffer_pie.seek(0)

img_buffer_comparecimento = io.BytesIO()
fig2.savefig(img_buffer_comparecimento, format='png', dpi=300, bbox_inches='tight')
img_buffer_comparecimento.seek(0)

output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_final.to_excel(writer, index=False, sheet_name='Dashboard', startrow=12)
    workbook = writer.book
    worksheet = writer.sheets['Dashboard']

    # ==== FORMATAÇÕES ====
    header_format = workbook.add_format({
        'bold': True, 'bg_color': '#004d00', 'font_color': 'white',
        'border': 1, 'align': 'center'
    })
    cell_format = workbook.add_format({'border': 1, 'align': 'center'})
    title_format = workbook.add_format({'bold': True, 'font_size': 14, 'font_color': '#004d00'})
    section_format = workbook.add_format({
        'bold': True, 'font_size': 11,
        'bg_color': '#d9ead3', 'border': 1,
        'align': 'center'
    })
    obs_format = workbook.add_format({'italic': True, 'font_color': '#555', 'bg_color': '#f0f0f0'})

    # ==== TÍTULO ====
    worksheet.merge_range('A1:G1', "📊 Indicadores Gerais", title_format)

    # ==== KPIs ====
    kpi_labels = [
        "✅ Aptos", "❌ Inaptos", "🚫 Desistentes",
        "🧮 Total", "📌 Agendados", "👥 % Comparecimento", "📉 % Inaptos"
    ]
    kpi_values = [
        total_aptos, total_inaptos, total_desistentes,
        total_geral, total_agendados,
        f"{taxa_comparecimento:.1f}%", f"{taxa_inaptos:.1f}%"
    ]
    worksheet.write_row('A2', kpi_labels, section_format)
    worksheet.write_row('A3', kpi_values, cell_format)
    worksheet.set_row(1, 20)
    worksheet.set_row(2, 24)

    # ==== TABELA ====
    for col_num, col_name in enumerate(df_final.columns):
        worksheet.write(12, col_num, col_name, header_format)
        worksheet.set_column(col_num, col_num, 20)
    for row in range(len(df_final)):
        for col in range(len(df_final.columns)):
            worksheet.write(row + 13, col, df_final.iloc[row, col], cell_format)

    # ==== GRÁFICOS ====
    worksheet.write('I2', "📊 Gráfico de Barras", section_format)
    worksheet.insert_image('I3', 'grafico_barras.png', {
        'image_data': img_buffer_bar, 'x_scale': 0.58, 'y_scale': 0.58
    })
    worksheet.write('I23', "🧩 Inaptos por Estudo", section_format)
    worksheet.insert_image('I24', 'grafico_pizza.png', {
        'image_data': img_buffer_pie, 'x_scale': 0.6, 'y_scale': 0.6
    })
    worksheet.write('I43', "🚷 Faltas x Comparecimentos", section_format)
    worksheet.insert_image('I44', 'grafico_comparecimento.png', {
        'image_data': img_buffer_comparecimento, 'x_scale': 0.6, 'y_scale': 0.6
    })

    # ==== OBSERVAÇÃO FINAL ====
    worksheet.merge_range('A30:G30',
        "Observação: Os dados refletem o status atualizado em 23/06/2025. "
        "O dashboard é gerado automaticamente pelo sistema de captação.",
        obs_format
    )

xlsx_data = output.getvalue()
st.download_button(
    label="📥 Baixar Dashboard em Excel",
    data=xlsx_data,
    file_name="dashboard_estudos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)