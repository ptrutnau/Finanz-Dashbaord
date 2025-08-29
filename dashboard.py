import streamlit as st
import pandas as pd
import plotly.express as px

# =====================
# Daten laden
# =====================
@st.cache_data
def load_data():
    df = pd.read_csv("finance_economics_dataset.csv", parse_dates=["Date"])
    return df

df = load_data()

# =====================
# Layout
# =====================
st.set_page_config(page_title="Finanz-Dashboard", layout="wide")
st.title("📊 Finanz-Dashboard")

# =====================
# Sidebar Filter
# =====================
st.sidebar.header("Filter")
indices = df["Stock Index"].unique().tolist()
selected_index = st.sidebar.selectbox("Wähle einen Index", indices)

date_min = df["Date"].min()
date_max = df["Date"].max()
date_range = st.sidebar.date_input("Zeitraum auswählen", [date_min, date_max])

# =====================
# Daten filtern
# =====================
filtered = df[df["Stock Index"] == selected_index]
filtered = filtered[(filtered["Date"] >= pd.to_datetime(date_range[0])) &
                    (filtered["Date"] <= pd.to_datetime(date_range[1]))]

# =====================
# Hauptbereich
# =====================
if not filtered.empty:
    # KPIs
    st.subheader("Wichtige Kennzahlen")
    col1, col2, col3 = st.columns(3)

    col1.metric("Letzter Schlusskurs", f"{filtered['Close Price'].iloc[-1]:.2f} USD")
    
    # Angepasste Darstellung des Handelsvolumens
    avg_volume_millions = filtered['Trading Volume'].mean() / 1_000_000
    col2.metric("Durchschn. Volumen", f"{avg_volume_millions:.2f} Mio")
    
    col3.metric("Durchschn. BIP-Wachstum", f"{filtered['GDP Growth (%)'].mean():.4f} %")

    # =====================
    # Charts
    # =====================
    st.subheader(f"Kursentwicklung – {selected_index}")

    fig = px.line(filtered, x="Date", y="Close Price", title="Schlusskurs über Zeit")
    st.plotly_chart(fig, use_container_width=True)

    # Zusatz-Chart: Makroindikatoren
    st.subheader("Makroökonomische Indikatoren")
    macro_option = st.selectbox("Wähle einen Indikator", [
        "GDP Growth (%)",
        "Inflation Rate (%)",
        "Unemployment Rate (%)",
        "Interest Rate (%)",
    ])

    fig2 = px.line(filtered, x="Date", y=macro_option, title=macro_option)
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("Keine Daten für den gewählten Zeitraum und Index gefunden.")

st.markdown("---")
st.caption("Datenquelle: [Finance and Economics Dataset (2000-Present)](https://www.kaggle.com/datasets/khushikyad001/finance-and-economics-dataset-2000-present) von Khushi")
st.caption("💡 Tipp: Du kannst dieses Dashboard später mit Streamlit Cloud teilen!")



