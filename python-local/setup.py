import duckdb
import os
from dataclasses import dataclass


@dataclass
class Student:
    id: int
    name: str
    program: str
    credits: int


def print_students(con):
    rows = con.execute(
        "SELECT id, name, program, credits FROM lake.students ORDER BY id"
    ).fetchall()
    for row in rows:
        print(f"  id={row[0]}, name={row[1]}, program={row[2]}, credits={row[3]}")


os.makedirs("lake-data", exist_ok=True)

con = duckdb.connect()
con.execute("INSTALL ducklake; LOAD ducklake")
con.execute("ATTACH 'ducklake:catalog.db' AS lake (DATA_PATH 'lake-data/')")
print("DuckLake is ready")

con.execute("""
    CREATE TABLE IF NOT EXISTS lake.students (
        id       INTEGER,
        name     VARCHAR NOT NULL,
        program  VARCHAR,
        credits  INTEGER
    )
""")
print("Table created: lake.students")

con.execute("DELETE FROM lake.students")

students = [
    Student(1, "Alice",   "Datateknik",    90),
    Student(2, "Bob",     "Medieteknik",   60),
    Student(3, "Charlie", "Elektroteknik", 45),
]

for s in students:
    con.execute(
        "INSERT INTO lake.students VALUES (?, ?, ?, ?)",
        [s.id, s.name, s.program, s.credits]
    )
print("Added 3 students")

print("\n--- After INSERT ---")
print_students(con)

con.execute("UPDATE lake.students SET credits = 75 WHERE id = 2")

print("\n--- After UPDATE ---")
print_students(con)

con.execute("DELETE FROM lake.students WHERE id = 3")

print("\n--- After DELETE ---")
print_students(con)

con.close()
print("\nDone! Check catalog.db and lake-data/ in your folder.")