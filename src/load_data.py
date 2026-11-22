from pathlib import Path
import sqlite3

from nycflights13 import flights, airlines, airports, weather

DB_PATH = Path("data/flights.db")


def build_database() -> None:
    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        flights.to_sql("flights", conn, if_exists="replace", index=False)
        airlines.to_sql("airlines", conn, if_exists="replace", index=False)
        airports.to_sql("airports", conn, if_exists="replace", index=False)
        weather.to_sql("weather", conn, if_exists="replace", index=False)
    print(f"Database creato in {DB_PATH}")


if __name__ == "__main__":
    build_database()
