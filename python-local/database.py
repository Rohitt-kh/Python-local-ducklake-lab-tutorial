import duckdb
import os

os.makedirs("lake-data", exist_ok=True)


def get_conn() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.execute("INSTALL ducklake; LOAD ducklake")
    con.execute("ATTACH 'ducklake:catalog.db' AS lake (DATA_PATH 'lake-data/')")
    return con