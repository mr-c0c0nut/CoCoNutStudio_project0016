import os
import json
import time
import uuid
import threading
from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "doi-key-nay-truoc-khi-deploy-that")

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
PLAYERS_PATH = os.path.join(DATA_DIR, "players.json")
VISITS_PATH = os.path.join(DATA_DIR, "visit_counter.json")

# ==========================================
# CẤU HÌNH BẢO MẬT (server-side only — KHÔNG bao giờ gửi các giá trị này ra frontend)
# ==========================================
# Đáp án của từng lớp được kiểm tra ở server. Trình duyệt chỉ nhận biết
# "đúng"/"sai" cho từng bước, không bao giờ thấy được đáp án thật.
# NÊN đặt qua biến môi trường khi deploy thật (Render > Environment),
# đừng để đáp án thật nằm cứng trong code commit lên git công khai —
# đặc biệt là LAYER4_ANSWER vì nó là link webhook Discord.
LAYER_ANSWERS = {
    1: os.environ.get("LAYER1_ANSWER", "doi-dap-an-lop-1-qua-bien-moi-truong"),
    2: os.environ.get("LAYER2_ANSWER", "doi-dap-an-lop-2-qua-bien-moi-truong"),
    3: os.environ.get("LAYER3_ANSWER", "0"),
    4: os.environ.get("LAYER4_ANSWER", "doi-dap-an-lop-4-qua-bien-moi-truong"),
}
TOTAL_LAYERS = 4

# ==========================================
# THEO DÕI LƯỢT TRUY CẬP THEO THỜI GIAN THỰC (RAM, không cần file riêng cho "online")
# ==========================================
_visitors_lock = threading.Lock()
_active_visitors = {}
ONLINE_WINDOW_SECONDS = 45  # coi là "đang online" nếu ping trong khoảng này

_stats_lock = threading.Lock()


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_total_visits():
    try:
        with open(VISITS_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("total_visits", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def _save_total_visits(value):
    _ensure_data_dir()
    with open(VISITS_PATH, "w", encoding="utf-8") as f:
        json.dump({"total_visits": value}, f)


def _touch_visitor():
    if "visitor_id" not in session:
        session["visitor_id"] = str(uuid.uuid4())
        with _stats_lock:
            _save_total_visits(_load_total_visits() + 1)
    with _visitors_lock:
        _active_visitors[session["visitor_id"]] = time.time()


def _count_online():
    now = time.time()
    with _visitors_lock:
        stale = [vid for vid, ts in _active_visitors.items() if now - ts > ONLINE_WINDOW_SECONDS]
        for vid in stale:
            del _active_visitors[vid]
        return len(_active_visitors)


# ==========================================
# DỮ LIỆU NGƯỜI CHƠI (lưu ra file JSON)
# ==========================================
# LƯU Ý: trên Render free tier, ổ đĩa là "ephemeral" — mỗi lần deploy lại
# hoặc service ngủ/thức dậy, file này có thể bị xoá sạch. Muốn dữ liệu bền
# thật sự (sống sót qua các lần deploy) cần Postgres/DB ngoài (vd. Supabase,
# Neon) hoặc Render Persistent Disk (gói trả phí), không phải file JSON.
def load_players():
    try:
        with open(PLAYERS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_players(players):
    _ensure_data_dir()
    with open(PLAYERS_PATH, "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=2)


# ==========================================
# HÀM THỐNG KÊ HỆ THỐNG (giữ nguyên như bản gốc)
# ==========================================
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
    # is_tech seed vào template để nếu đã đăng nhập từ trước (session còn),
    # trang tự mở sẵn bảng điều khiển mà không cần gọi thêm API rồi mới hiện.
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
    correct = given == expected.replace(" ", "") if step == 2 else given == expected

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
        "total_visits": _load_total_visits(),
        "players_count": len(load_players()),
    })


if __name__ == "__main__":
    _ensure_data_dir()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
