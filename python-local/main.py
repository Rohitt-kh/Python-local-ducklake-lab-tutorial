from fastapi import FastAPI
from database import get_conn
from student import Student

app = FastAPI(title="DuckLake Local API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/datasets")
def list_datasets():
    with get_conn() as con:
        tables = con.execute(
            "SELECT table_name FROM duckdb_tables() WHERE database_name = 'lake'"
        ).fetchall()
    return [{"name": r[0]} for r in tables]


@app.get("/datasets/students")
def get_students():
    with get_conn() as con:
        rows = con.execute(
            "SELECT id, name, program, credits FROM lake.students ORDER BY id"
        ).fetchall()
    return [Student(id=r[0], name=r[1], program=r[2], credits=r[3]) for r in rows]