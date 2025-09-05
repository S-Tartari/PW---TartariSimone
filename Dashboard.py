import os
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Titolo
def DashTitle():
    st.set_page_config(
        page_title="Dashboard",
        page_icon="🏔️",
        layout="wide"
    )
    st.title("🏔️ Sempre più in Alto!")
    st.markdown("##### Dashboard per analisi della produzione aziendale")

# Note finali
def FinalNotes():
    st.markdown("""
    ---
    Simone TARTARI - Matricola 0312201761  
    Laurea Triennale in Informatica per le Aziende Digitali (L-31)
    """)

#*** START ***
DashTitle()
csv_file = "Prodotti.csv"                # Caricamento file

if not os.path.exists(csv_file):         # Controllo dell'esistenza del file, altrimenti blocca esecuzione
    st.error(f"File '{csv_file}' non trovato.")
    st.stop()

df = pd.read_csv(csv_file)

#*** Sidebar ***
st.sidebar.header("Filtri")

if "Time" in df.columns:                 # Controlla se esiste la colonna 'Time' per applicare il filtro
    periodi = df["Time"].tolist()
    periodo_sel = st.sidebar.slider(
        "Seleziona periodo massimo",
        min_value=min(periodi),
        max_value=max(periodi),
        value=max(periodi)
    )
    df = df[df["Time"] <= periodo_sel]   # Applica filtro sul periodo massimo selezionato

# Altri filtri
settimane = sorted(df["Settimana"].unique())        # Estrae e ordina le settimane presenti nel file
prodotti = sorted(df["Articolo"].unique())          # Estrae e ordina i nomi dei prodotti presenti nel file

# Slider per selezionare range di settimane
week_min, week_max = st.sidebar.slider(
    "Settimane (intervallo)",
    min_value=min(settimane),
    max_value=max(settimane),
    value=(min(settimane), max(settimane)),
    step=1
)

# Radio per selezionare singolo Articolo o "Tutti" da analizzare
prod_select = st.sidebar.multiselect(
    "Prodotti (selezione multipla)",
    options=prodotti,
    default=prodotti,
    key="prodotti_multiselect"
)

# Applica filtri
filtered_df = df[
    df["Settimana"].between(week_min, week_max) &
    df["Articolo"].isin(prod_select)
    ]

#*** KPI Dinamici ***
st.subheader("📊 Indicatori globali")

col1, col2, col3, col4 = st.columns(4)

# Ordini ricevuti (sommati per Articolo)
ordini_ricevuti = filtered_df.groupby("Articolo")["Art. ordinati"].sum()

# Ordini spediti (sommati per Articolo)
ordini_spediti = filtered_df.groupby("Articolo")["Art. spediti"].sum()

# Ordini scartati (sommati per Articolo)
ordini_scartati = filtered_df.groupby("Articolo")["Art. scartati"].sum()

# Overstock (sommati per Articolo)
overstock = filtered_df.groupby("Articolo")["Overstock t1"].sum()

with col1:
    st.metric("📥 Ordini ricevuti", int(ordini_ricevuti.sum()))
    st.dataframe(ordini_ricevuti, use_container_width=True)

with col2:
    st.metric("🚛 Ordini spediti", int(ordini_spediti.sum()))
    st.dataframe(ordini_spediti, use_container_width=True)

with col3:
    st.metric("🗑️ Articoli prodotti scartati", int(ordini_scartati.sum()))
    st.dataframe(ordini_scartati, use_container_width=True)

with col4:
    st.metric("📈 Overstock per Articolo",int(overstock.sum()))
    st.dataframe(overstock, use_container_width=True)


col5, col6, col7, col8 = st.columns(4)

# Stock iniziale (prima settimana del range)
stock_iniziale = (
    filtered_df[filtered_df["Settimana"] == week_min]
    .groupby("Articolo")["Stock"]
    .sum()
)

# Stock finale (ultima settimana del range)
stock_finale = (
    filtered_df[filtered_df["Settimana"] == week_max]
    .groupby("Articolo")["Stock finale"]
    .sum()
)

# Backlog iniziale (prima settimana del range)
backlog_iniziale = (
    filtered_df[filtered_df["Settimana"] == week_min]
    .groupby("Articolo")["Backlog"]
    .sum()
)

# Backlog finale (ultima settimana del range)
backlog_finale = (
    filtered_df[filtered_df["Settimana"] == week_max]
    .groupby("Articolo")["Backlog finale"]
    .sum()
)

with col5:
    st.metric("📦 Stock Iniziale",int(stock_iniziale.sum()))
    st.dataframe(stock_iniziale, use_container_width=True)

with col6:
    st.metric("📦 Stock finale", int(stock_finale.sum()))
    st.dataframe(stock_finale, use_container_width=True)

with col7:
    st.metric("⚠️ Backlog iniziale", int(backlog_iniziale.sum()))
    st.dataframe(backlog_iniziale, use_container_width=True)

with col8:
    st.metric("⚠️ Backlog finale", int(backlog_finale.sum()))
    st.dataframe(backlog_finale, use_container_width=True)

#*** Grafico efficienza produttiva per articolo ***
st.subheader("⚙️ Efficienza produttiva per articolo")

# Calcolo efficienza per riga
df_eff = filtered_df.copy()
df_eff["Ore teoriche produzione"] = df_eff["Art. prodotti"] * df_eff["Ore articolo"]                 # Calcolo delle ore teoriche necessarie alla produzione
df_eff["Efficienza (%)"] = (df_eff["Ore teoriche produzione"] / df_eff["Ore settimanali"]) * 100     # Calcolo dell'efficienza come rapporto tra ore teoriche e disponibili

# Raggruppamento per settimana e articolo
eff_grouped = df_eff.groupby(["Settimana", "Articolo"])["Efficienza (%)"].mean().reset_index()

# Aggiunta descrizione
st.markdown("🛈 *Se la performance è bassa, significa che si produce molto overstock rispetto agli ordini richiesti.*")

# Grafico a linee per articolo
fig = px.line(
    eff_grouped,
    x="Settimana",
    y="Efficienza (%)",
    color="Articolo",
    markers=True,
    line_shape="linear"
)
fig.update_layout(
    xaxis_title="Settimana",
    yaxis_title="Efficienza (%)",
    xaxis=dict(tickmode="linear", dtick=1),
    margin=dict(t=30)
)
st.plotly_chart(fig, use_container_width=True)

#*** Grafico a barre: prodotti per settimana ***
st.subheader("🏭 Articoli prodotti per settimana")

# Somma delle due colonne per ogni combinazione di Settimana e Articolo
filtered_df["Totale prodotti"] = filtered_df["Art. prodotti"] + filtered_df["Overstock t1"]

# Raggruppamento per settimana e articolo
dati = filtered_df.groupby(["Settimana", "Articolo"])["Totale prodotti"].sum().reset_index()

# Creazione del grafico
fig = px.bar(dati, x="Settimana", y="Totale prodotti", color="Articolo", barmode="stack")
fig.update_layout(xaxis_tickangle=0, margin=dict(t=30))

st.plotly_chart(fig, use_container_width=True)

#*** Grafico lineare: prodotti spediti nel tempo ***
st.subheader("🚛 Articoli spediti nel tempo")

dati = filtered_df.groupby(["Settimana", "Articolo"])["Art. spediti"].sum().reset_index()

fig = px.line(dati, x="Settimana", y="Art. spediti", color="Articolo", markers=True)      # Creazione grafico a linee degli articoli spediti nel tempo
fig.update_layout(
    xaxis_title="Settimana",
    yaxis_title="Articoli spediti",
    xaxis_tickformat=",d",                      # solo interi
    xaxis=dict(tickmode="linear", dtick=1),
    margin=dict(t=30)
)

st.plotly_chart(fig, use_container_width=True)

 #*** Grafico lineare: Funzioni aziendali ***
st.sidebar.header("Funzioni aziendali")

# Stato sessione
if "selected_group" not in st.session_state:
            st.session_state.selected_group = "Sales Office"

# Settori e variabili predefinite
column_groups = {
    "Sales Office": ["Backlog", "Art. ordinati", "Art. da produrre", "Art. per Logistica", "Backlog finale"],
     "Production": ["Art. prodotti", "Overstock", "Ore totali", "Ore disponibili"],
     "Quality": ["Art. per CQ", "Art. scartati", "Art. passed", "Overstock t1"],
     "Logistics": ["Art. da spedire", "Art. spediti"],
      "Warehouse": ["Stock", "Stock finale"],
     }

# Scelta gruppo
selected_group = st.sidebar.radio(
    "Seleziona funzione:",
    options=list(column_groups.keys()),
    index=list(column_groups.keys()).index(st.session_state.selected_group),
    key="group_selection",
    )
st.session_state.selected_group = selected_group
st.sidebar.markdown("---")

# Scelta variabili
variabili = st.sidebar.multiselect(
    "Variabili da mostrare",
    options=filtered_df.columns[1:],  # esclude la prima colonna se è un id
    default=[v for v in column_groups[selected_group] if v in filtered_df.columns],
    key="variabili_funz_az",
    )

st.subheader(f"📊 {selected_group} - Andamento delle variabili")

# Variabili realmente presenti nel dataframe
variabili_valid = [v for v in variabili if v in filtered_df.columns]

def _to_num(s):
    # Converte stringhe con '%' in numeri, altrimenti prova coerzione diretta
    if s.dtype == "object":
        return pd.to_numeric(s.astype(str).str.replace("%", ""), errors="coerce")
    return pd.to_numeric(s, errors="coerce")

if variabili_valid:
    # Grafico
    fig, ax = plt.subplots(figsize=(8, 4))

    # Converte in numerico solo le colonne selezionate (più leggero)
    df_num = filtered_df[["Settimana"] + variabili_valid].copy()
    for v in variabili_valid:
        df_num[v] = _to_num(df_num[v])

    for v in variabili_valid:
        ax.plot(df_num["Settimana"], df_num[v], marker="o", label=v)

  # Formattazione degli assi
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=0)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("Selezionare una Funzione Aziendale nel menu a sinistra.")
    
# --- Tabella dei dati filtrati ---
with st.expander("📄 Mostra tabella dati"):
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# --- Footer ---
FinalNotes()