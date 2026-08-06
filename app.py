import os
import json
import time
import uuid
import hmac
import sqlite3
import threading
from flask import Flask, render_template, request, session, jsonify
from dotenv import load_dotenv

# Tự động đọc file .env ở môi trường local
load_dotenv()

app = Flask(__name__)
# Đảm bảo SECRET_KEY luôn cố định qua biến môi trường
app.secret_key = os.environ.get("SECRET_KEY", "key-mac-dinh-de-test-local-123456")

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "storage.db")

# ==========================================
# CẤU HÌNH BẢO MẬT
# ==========================================
LAYER_ANSWERS = {
    1: os.environ.get("LAYER1_ANSWER", "dap-an-lop-1"),
    2: os.environ.get("LAYER2_ANSWER", "dap-an-lop-2"),
    3: os.environ.get("LAYER3_ANSWER", "0"),
    4: os.environ.get("LAYER4_ANSWER", "dap-an-lop-4"),
}
TOTAL_LAYERS = 4

# ==========================================
# CƠ SỞ DỮ LIỆU TỰ ĐỘNG & BỀN VỮNG (SQLITE WAL)
# ==========================================
def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    with get_db_connection() as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                key TEXT PRIMARY KEY,
                value INTEGER DEFAULT 0
            )
        """)
        conn.execute("INSERT OR IGNORE INTO stats (key, value) VALUES ('total_visits', 0)")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players_storage (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                data TEXT NOT NULL
            )
        """)
        conn.execute("INSERT OR IGNORE INTO players_storage (id, data) VALUES (1, '[]')")
        conn.commit()

init_db()

def increment_visits():
    with get_db_connection() as conn:
        conn.execute("UPDATE stats SET value = value + 1 WHERE key = 'total_visits'")
        conn.commit()

def load_total_visits():
    with get_db_connection() as conn:
        row = conn.execute("SELECT value FROM stats WHERE key = 'total_visits'").fetchone()
        return row["value"] if row else 0

def load_players():
    try:
        with get_db_connection() as conn:
            row = conn.execute("SELECT data FROM players_storage WHERE id = 1").fetchone()
            return json.loads(row["data"]) if row else []
    except Exception:
        return []

def save_players(players_list):
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE players_storage SET data = ? WHERE id = 1",
            (json.dumps(players_list, ensure_ascii=False),)
        )
        conn.commit()

# ==========================================
# THEO DÕI VISITOR REALTIME
# ==========================================
_visitors_lock = threading.Lock()
_active_visitors = {}
ONLINE_WINDOW_SECONDS = 45

def _touch_visitor():
    if "visitor_id" not in session:
        session["visitor_id"] = str(uuid.uuid4())
        increment_visits()
        
    with _visitors_lock:
        _active_visitors[session["visitor_id"]] = time.time()

def _count_online():
    now = time.time()
    with _visitors_lock:
        stale = [vid for vid, ts in _active_visitors.items() if now - ts > ONLINE_WINDOW_SECONDS]
        for vid in stale:
            del _active_visitors[vid]
        return len(_active_visitors)

def get_system_stats():
    return {
        "active_testers": "30+",
        "tested_players": "1.800+",
        "completed_tests": "5.200+",
    }

# ==========================================
# ROUTES
# ==========================================
@app.route("/")
def home():
    _touch_visitor()
    stats = get_system_stats()
    return render_template("index.html", stats=stats, is_tech=bool(session.get("is_tech")))

@app.route("/api/heartbeat", methods=["POST"])
def heartbeat():
    _touch_visitor()
    return jsonify({"online": _count_online()})

@app.route("/api/unlock/step", methods=["POST"])
def unlock_step():
    data = request.get_json(silent=True) or {}
    step = data.get("step")
    answer = (data.get("answer") or "").strip()

    if step not in (1, 2, 3, 4):
        return jsonify({"ok": False, "error": "invalid_step"}), 400

    progress = session.get("unlock_progress", 0)
    if step != progress + 1:
        return jsonify({"ok": False, "error": "out_of_order"}), 400

    expected = str(LAYER_ANSWERS[step]).strip()
    given = answer.replace(" ", "") if step == 2 else answer
    expected_cmp = expected.replace(" ", "") if step == 2 else expected

    correct = hmac.compare_digest(given, expected_cmp)

    if not correct:
        return jsonify({"ok": False, "passed": False})

    session["unlock_progress"] = step
    if step == TOTAL_LAYERS:
        session["is_tech"] = True

    return jsonify({"ok": True, "passed": True, "unlocked": session.get("is_tech", False)})

@app.route("/api/unlock/reset", methods=["POST"])
def unlock_reset():
    session.pop("unlock_progress", None)
    session.pop("is_tech", None)
    return jsonify({"ok": True})

@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    session.pop("is_tech", None)
    session.pop("unlock_progress", None)
    return jsonify({"ok": True})

@app.route("/api/players", methods=["GET"])
def get_players():
    if not session.get("is_tech"):
        return jsonify({"ok": False, "error": "unauthorized"}), 403
    return jsonify(load_players())

@app.route("/api/players", methods=["POST"])
def set_players():
    if not session.get("is_tech"):
        return jsonify({"ok": False, "error": "unauthorized"}), 403
    data = request.get_json(silent=True) or {}
    players = data.get("players")
    if not isinstance(players, list):
        return jsonify({"ok": False, "error": "invalid_payload"}), 400
    save_players(players)
    return jsonify({"ok": True, "count": len(players)})

@app.route("/api/admin/stats")
def admin_stats():
    if not session.get("is_tech"):
        return jsonify({"ok": False, "error": "unauthorized"}), 403
    return jsonify({
        "ok": True,
        "online_now": _count_online(),
        "total_visits": load_total_visits(),
        "players_count": len(load_players()),
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
