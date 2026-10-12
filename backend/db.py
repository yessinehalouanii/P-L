import json
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "data" / "steps.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_name TEXT NOT NULL,
            source_key TEXT NOT NULL,
            period TEXT,
            payload TEXT NOT NULL,
            source_file TEXT,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_records_source ON records(source_key);
        CREATE INDEX IF NOT EXISTS idx_records_property ON records(property_name);
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_name TEXT NOT NULL,
            title TEXT NOT NULL,
            domain TEXT,
            owner TEXT,
            priority TEXT,
            due_date TEXT,
            target TEXT,
            guardrail TEXT,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_name TEXT NOT NULL,
            domain TEXT,
            title TEXT NOT NULL,
            evidence TEXT,
            recommendation TEXT,
            impact TEXT,
            confidence INTEGER,
            status TEXT NOT NULL DEFAULT 'Draft',
            created_at TEXT NOT NULL
        );
        """)

def add_record(property_name, source_key, payload, period=None, source_file=None):
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO records(property_name, source_key, period, payload, source_file, created_at) VALUES(?,?,?,?,?,?)",
            (property_name, source_key, period, json.dumps(payload, default=str), source_file, datetime.utcnow().isoformat())
        )
        return cur.lastrowid

def add_records(property_name, source_key, rows, period=None, source_file=None):
    now = datetime.utcnow().isoformat()
    with connect() as conn:
        conn.executemany(
            "INSERT INTO records(property_name, source_key, period, payload, source_file, created_at) VALUES(?,?,?,?,?,?)",
            [(property_name, source_key, period, json.dumps(r, default=str), source_file, now) for r in rows]
        )
    return len(rows)

def get_records(source_key=None, property_name="Harbour Crest Resort", limit=5000):
    q = "SELECT * FROM records WHERE property_name=?"
    params = [property_name]
    if source_key:
        q += " AND source_key=?"
        params.append(source_key)
    q += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    with connect() as conn:
        rows = conn.execute(q, params).fetchall()
    out = []
    for row in rows:
        item = dict(row)
        item["payload"] = json.loads(item["payload"])
        out.append(item)
    return out

def record_counts(property_name="Harbour Crest Resort"):
    with connect() as conn:
        rows = conn.execute("SELECT source_key, COUNT(*) n, MAX(created_at) last_update FROM records WHERE property_name=? GROUP BY source_key", (property_name,)).fetchall()
    return {r["source_key"]: {"count": r["n"], "last_update": r["last_update"]} for r in rows}

def add_action(data):
    with connect() as conn:
        cur = conn.execute("""
            INSERT INTO actions(property_name,title,domain,owner,priority,due_date,target,guardrail,status,created_at)
            VALUES(?,?,?,?,?,?,?,?,?,?)
        """, (
            data.get("property_name","Harbour Crest Resort"), data["title"], data.get("domain"), data.get("owner"),
            data.get("priority","Medium"), data.get("due_date"), data.get("target"), data.get("guardrail"),
            data.get("status","Open"), datetime.utcnow().isoformat()
        ))
        return cur.lastrowid

def get_actions(property_name="Harbour Crest Resort"):
    with connect() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM actions WHERE property_name=? ORDER BY id DESC", (property_name,)).fetchall()]

def replace_recommendations(property_name, recs):
    with connect() as conn:
        conn.execute("DELETE FROM recommendations WHERE property_name=?", (property_name,))
        now = datetime.utcnow().isoformat()
        conn.executemany("""
            INSERT INTO recommendations(property_name,domain,title,evidence,recommendation,impact,confidence,status,created_at)
            VALUES(?,?,?,?,?,?,?,?,?)
        """, [(property_name, r['domain'], r['title'], json.dumps(r['evidence']), r['recommendation'], r['impact'], r['confidence'], 'Draft', now) for r in recs])

def get_recommendations(property_name="Harbour Crest Resort"):
    with connect() as conn:
        rows = conn.execute("SELECT * FROM recommendations WHERE property_name=? ORDER BY confidence DESC, id", (property_name,)).fetchall()
    out=[]
    for r in rows:
        x=dict(r); x['evidence']=json.loads(x['evidence'] or '[]'); out.append(x)
    return out

def set_recommendation_status(rec_id, status):
    with connect() as conn:
        conn.execute("UPDATE recommendations SET status=? WHERE id=?", (status, rec_id))
