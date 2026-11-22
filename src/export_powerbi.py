"""Esporta in CSV le tabelle per Power BI, eseguendo le query di sql/06_export_powerbi.sql."""
import argparse
import re
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "flights.db"
SQL_FILE = ROOT / "sql" / "06_export_powerbi.sql"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(ROOT / "exports" / "powerbi"), help="cartella di destinazione dei CSV")
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # Il file SQL contiene più query, ognuna preceduta da "-- name: nome_tabella"
    parts = re.split(r"^-- name: (.+)$", SQL_FILE.read_text(), flags=re.MULTILINE)
    with sqlite3.connect(DB_PATH) as conn:
        for name, sql in zip(parts[1::2], parts[2::2]):
            df = pd.read_sql(sql, conn)
            path = out / f"{name}.csv"
            df.to_csv(path, index=False)
            print(f"{path}: {len(df):,} righe")


if __name__ == "__main__":
    main()