"""
Simple SQLite persistence thay thế file JSON.
Dùng sqlite3 built-in, không cần thêm dependency.
"""
import sqlite3
import json
import os

DB_PATH = os.environ.get("DB_PATH", "orders.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                data TEXT NOT NULL
            )
        """)
        conn.commit()

def load_orders() -> list[dict]:
    init_db()
    with get_conn() as conn:
        rows = conn.execute("SELECT data FROM orders ORDER BY id").fetchall()
        return [json.loads(r["data"]) for r in rows]

def save_order(order_dict: dict):
    init_db()
    with get_conn() as conn:
        existing = conn.execute("SELECT id FROM orders WHERE id=?", (order_dict["id"],)).fetchone()
        if existing:
            conn.execute("UPDATE orders SET data=? WHERE id=?",
                        (json.dumps(order_dict, default=str), order_dict["id"]))
        else:
            conn.execute("INSERT INTO orders (id, data) VALUES (?,?)",
                        (order_dict["id"], json.dumps(order_dict, default=str)))
        conn.commit()

def update_order(order_id: int, updates: dict):
    init_db()
    with get_conn() as conn:
        row = conn.execute("SELECT data FROM orders WHERE id=?", (order_id,)).fetchone()
        if row:
            data = json.loads(row["data"])
            data.update(updates)
            conn.execute("UPDATE orders SET data=? WHERE id=?",
                        (json.dumps(data, default=str), order_id))
            conn.commit()
            return data
    return None

def next_id() -> int:
    init_db()
    with get_conn() as conn:
        row = conn.execute("SELECT MAX(id) as max_id FROM orders").fetchone()
        return (row["max_id"] or 0) + 1
