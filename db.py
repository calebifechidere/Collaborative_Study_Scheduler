import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    # Online deployment: Neon
    if database_url:
        return psycopg.connect(database_url)

    # Local development: Docker PostgreSQL
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "study_scheduler"),
        user=os.getenv("DB_USER", "scheduler_user"),
        password=os.getenv("DB_PASSWORD", "scheduler_password"),
    )


def fetch_all(query, params=()):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            columns = [col.name for col in cur.description] if cur.description else []
            rows = cur.fetchall()
            return [dict(zip(columns, row)) for row in rows]


def fetch_one(query, params=()):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            columns = [col.name for col in cur.description] if cur.description else []
            row = cur.fetchone()
            if row is None:
                return None
            return dict(zip(columns, row))


def execute(query, params=()):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
            return cur.rowcount


def execute_with_row(query, params=()):
    conn = get_connection()
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
            cur.execute(query, params)
            row = cur.fetchone()
            conn.commit()
            return row
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def start_transaction():
    conn = get_connection()
    conn.autocommit = False
    return conn


def commit_transaction(conn):
    conn.commit()
    conn.close()


def rollback_transaction(conn):
    conn.rollback()
    conn.close()
