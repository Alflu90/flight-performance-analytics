import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "flights.db"
KEYS = ["origin", "year", "month", "day", "hour"]

st.set_page_config(page_title="Flight Performance Analytics", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        flights = pd.read_sql(
            "SELECT origin, carrier, year, month, day, hour, dep_delay, arr_delay FROM flights",
            conn,
        )
        airlines = pd.read_sql("SELECT carrier, name AS compagnia FROM airlines", conn)
        weather = pd.read_sql(f"SELECT {', '.join(KEYS)}, precip FROM weather", conn)
    df = flights.merge(airlines, on="carrier", how="left")
    df = df.merge(weather, on=KEYS, how="left")
    df["pioggia"] = df["precip"] > 0
    return df


df = load_data()

st.title("Flight Performance Analytics")
st.caption("Dataset nycflights13 (voli da New York, 2013). In ritardo = oltre 15 minuti.")

origins = st.sidebar.multiselect(
    "Aeroporto di partenza", sorted(df["origin"].unique()), default=sorted(df["origin"].unique())
)
df = df[df["origin"].isin(origins)]

dep = df.dropna(subset=["dep_delay"]).copy()
dep["in_ritardo"] = dep["dep_delay"] > 15

c1, c2, c3, c4 = st.columns(4)
c1.metric("Voli (con partenza registrata)", f"{len(dep):,}")
c2.metric("% partenze in ritardo", f"{100 * dep['in_ritardo'].mean():.1f}%")
c3.metric("Ritardo medio (min)", f"{dep['dep_delay'].mean():.1f}")
c4.metric("Ritardo mediano (min)", f"{dep['dep_delay'].median():.1f}")

left, right = st.columns(2)

with left:
    st.subheader("% partenze in ritardo per ora programmata")
    per_ora = dep.groupby("hour")["in_ritardo"].mean().mul(100)
    st.bar_chart(per_ora)

with right:
    st.subheader("Pioggia vs no pioggia")
    pioggia = (
        dep.dropna(subset=["pioggia"])
        .groupby("pioggia")["in_ritardo"]
        .mean()
        .mul(100)
        .rename(index={False: "No pioggia", True: "Pioggia"})
    )
    st.bar_chart(pioggia)

st.subheader("Compagnie (ritardo all'arrivo)")
arr = df.dropna(subset=["arr_delay"]).copy()
arr["in_ritardo"] = arr["arr_delay"] > 15
compagnie = (
    arr.groupby("compagnia")
    .agg(
        voli=("arr_delay", "size"),
        ritardo_medio=("arr_delay", "mean"),
        perc_in_ritardo=("in_ritardo", lambda s: 100 * s.mean()),
    )
    .round(2)
    .sort_values("ritardo_medio")
)
st.dataframe(compagnie[compagnie["voli"] >= 1000], use_container_width=True)
st.caption("Mostrate solo le compagnie con almeno 1.000 voli.")