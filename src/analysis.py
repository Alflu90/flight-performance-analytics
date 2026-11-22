import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "flights.db"
DELAY_THRESHOLD = 15  # minuti: oltre questa soglia un volo è "in ritardo"


def load_table(name: str, db_path: Path = DB_PATH) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql(f"SELECT * FROM {name}", conn)


def add_delay_flag(df: pd.DataFrame, delay_col: str) -> pd.DataFrame:
    """Elimina i voli senza dato di ritardo e aggiunge la colonna booleana in_ritardo."""
    out = df.dropna(subset=[delay_col]).copy()
    out["in_ritardo"] = out[delay_col] > DELAY_THRESHOLD
    return out


def summarize_delays(df: pd.DataFrame, by, delay_col: str, min_flights: int = 0) -> pd.DataFrame:
    """Voli, media, mediana e % in ritardo per gruppo."""
    df = add_delay_flag(df, delay_col)
    summary = (
        df.groupby(by, observed=True)
        .agg(
            voli=(delay_col, "size"),
            media=(delay_col, "mean"),
            mediana=(delay_col, "median"),
            perc_ritardo=("in_ritardo", lambda s: 100 * s.mean()),
        )
        .round(2)
    )
    return summary[summary["voli"] >= min_flights]