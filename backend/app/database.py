"""
Database layer — PostgreSQL (production) hoặc SQLite (local dev).
"""
import json
import os
import sqlite3

DATABASE_URL = os.environ.get("DATABASE_URL", "")

# ── PostgreSQL ────────────────────────────────────────────────────────────────
if DATABASE_URL and DATABASE_URL.startswith("postgres"):
    import psycopg2
    import psycopg2.extras
    from psycopg2 import pool as pg_pool

    # Fix URL format
    _db_url = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    # Connection pool
    _pool = None

    def get_pool():
        global _pool
        if _pool is None or _pool.closed:
            _pool = pg_pool.SimpleConnectionPool(1, 5, _db_url,
                connect_timeout=10,
                options="-c statement_timeout=30000"
            )
        return _pool

    def get_conn():
        return get_pool().getconn()

    def release_conn(conn):
        try:
            get_pool().putconn(conn)
        except Exception:
            pass

    def init_db():
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        id SERIAL PRIMARY KEY,
                        data JSONB NOT NULL
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS reviews (
                        id SERIAL PRIMARY KEY,
                        data JSONB NOT NULL
                    )
                """)
            conn.commit()
        finally:
            release_conn(conn)

    def load_orders() -> list[dict]:
        init_db()
        conn = get_conn()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT data FROM orders ORDER BY id")
                return [dict(r["data"]) for r in cur.fetchall()]
        finally:
            release_conn(conn)

    def save_order(order_dict: dict):
        init_db()
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM orders WHERE (data->>'id')::int = %s", (order_dict["id"],))
                if cur.fetchone():
                    cur.execute("UPDATE orders SET data=%s WHERE (data->>'id')::int=%s",
                                (json.dumps(order_dict, default=str), order_dict["id"]))
                else:
                    cur.execute("INSERT INTO orders (data) VALUES (%s)",
                                (json.dumps(order_dict, default=str),))
            conn.commit()
        finally:
            release_conn(conn)

    def update_order(order_id: int, updates: dict):
        init_db()
        conn = get_conn()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT data FROM orders WHERE (data->>'id')::int=%s", (order_id,))
                row = cur.fetchone()
                if not row:
                    return None
                data = dict(row["data"])
                data.update(updates)
                cur.execute("UPDATE orders SET data=%s WHERE (data->>'id')::int=%s",
                            (json.dumps(data, default=str), order_id))
            conn.commit()
            return data
        finally:
            release_conn(conn)

    def next_id() -> int:
        init_db()
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COALESCE(MAX((data->>'id')::int), 0) FROM orders")
                return (cur.fetchone()[0] or 0) + 1
        finally:
            release_conn(conn)

    def load_reviews(product_id: int) -> list[dict]:
        init_db()
        conn = get_conn()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT data FROM reviews WHERE (data->>'product_id')::int=%s ORDER BY id DESC", (product_id,))
                return [dict(r["data"]) for r in cur.fetchall()]
        finally:
            release_conn(conn)

    def save_review(review_dict: dict):
        init_db()
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO reviews (data) VALUES (%s)",
                            (json.dumps(review_dict, default=str),))
            conn.commit()
        finally:
            release_conn(conn)

# ── SQLite fallback (local dev) ───────────────────────────────────────────────
else:
    DB_PATH = os.environ.get("DB_PATH", "orders.db")

    def get_conn():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db():
        with get_conn() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, data TEXT NOT NULL)")
            conn.execute("CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY, data TEXT NOT NULL)")
            conn.commit()

    def load_orders() -> list[dict]:
        init_db()
        with get_conn() as conn:
            return [json.loads(r["data"]) for r in conn.execute("SELECT data FROM orders ORDER BY id").fetchall()]

    def save_order(order_dict: dict):
        init_db()
        with get_conn() as conn:
            if conn.execute("SELECT id FROM orders WHERE id=?", (order_dict["id"],)).fetchone():
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
            if not row:
                return None
            data = json.loads(row["data"])
            data.update(updates)
            conn.execute("UPDATE orders SET data=? WHERE id=?",
                         (json.dumps(data, default=str), order_id))
            conn.commit()
            return data

    def next_id() -> int:
        init_db()
        with get_conn() as conn:
            row = conn.execute("SELECT MAX(id) as m FROM orders").fetchone()
            return (row["m"] or 0) + 1

    def load_reviews(product_id: int) -> list[dict]:
        init_db()
        with get_conn() as conn:
            rows = conn.execute("SELECT data FROM reviews WHERE json_extract(data,'$.product_id')=? ORDER BY id DESC", (product_id,)).fetchall()
            return [json.loads(r["data"]) for r in rows]

    def save_review(review_dict: dict):
        init_db()
        with get_conn() as conn:
            conn.execute("INSERT INTO reviews (data) VALUES (?)", (json.dumps(review_dict, default=str),))
            conn.commit()
