
KHÔNG sửa các API khác nếu không cần.

KHÔNG giải thích.

KHÔNG chia nhỏ.

KHÔNG dùng canvas.

KHÔNG dùng pseudo code.

KHÔNG dùng "ví dụ".

Chỉ trả về code hoàn chỉnh.



==========================

YÊU CẦU

==========================



1. Xóa hoàn toàn hệ thống lưu players.json.



Xóa:



PLAYERS_PATH



_init_players_cache()



save_all_players()



mọi thao tác đọc ghi players.json.



Server restart thì dữ liệu player mất hoàn toàn.



==========================



2. Chỉ lưu player trong RAM.



Dùng:



_players_lock = threading.Lock()



_PLAYERS = {}



Không dùng list.



Key là tên player.



Ví dụ:



_PLAYERS = {

    "Steve":{

        "name":"Steve",

        "avatar":"https://...",

        "tier":"HT2",

        "point":60

    }

}



==========================



3. Chỉ có 4 trường dữ liệu



name

avatar

tier

point



Không thêm field khác.



==========================



4. point KHÔNG được frontend gửi.



Backend tự tính theo bảng:



TIER_POINTS = {

    "LT5": 10,

    "HT5": 15,

    "LT4": 20,

    "HT4": 25,

    "LT3": 30,

    "HT3": 40,

    "LT2": 50,

    "HT2": 60,

    "LT1": 70,

    "HT1": 80

}



Nếu tier đổi thì point đổi tự động.



==========================



5. GET /api/players



Trả về list player.



==========================



6. POST /api/players



Frontend vẫn gửi nguyên list player như project cũ.



Server sẽ:



- clear _PLAYERS



- normalize dữ liệu



- lưu vào RAM



Không ghi file.



==========================



7. Tạo hàm normalize.



Nếu tier sai



=> LT5



Nếu name rỗng



=> bỏ qua.



point luôn lấy từ TIER_POINTS.



==========================



8. Không đụng tới



unlock



heartbeat



visitor



admin



session



online counter



security layer



home page



stats



==========================



9. Giữ nguyên tất cả route hiện có.



Không đổi tên API.



Không đổi response JSON.



Không phá frontend hiện tại.



==========================



10. Trả về duy nhất app.py hoàn chỉnh.



Không giải thích.



Không markdown.



Không nói "đây là code".



Chỉ in nguyên nội dung file app.py.



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

# CẤU HÌNH BẢO MẬT

# ==========================================

LAYER_ANSWERS = {

    1: os.environ.get("LAYER1_ANSWER", "doi-dap-an-lop-1-qua-bien-moi-truong"),

    2: os.environ.get("LAYER2_ANSWER", "doi-dap-an-lop-2-qua-bien-moi-truong"),

    3: os.environ.get("LAYER3_ANSWER", "0"),

    4: os.environ.get("LAYER4_ANSWER", "doi-dap-an-lop-4-qua-bien-moi-truong"),

}

TOTAL_LAYERS = 4



# ==========================================

# THEO DÕI LƯỢT TRUY CẬP & ONLINE

# ==========================================

_visitors_lock = threading.Lock()

_active_visitors = {}

ONLINE_WINDOW_SECONDS = 45



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

    try:

        _ensure_data_dir()

        with open(VISITS_PATH, "w", encoding="utf-8") as f:

            json.dump({"total_visits": value}, f)

    except Exception:

        pass





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

# BỘ NHỚ LƯU PLAYER (RAM + FILE JSON BACKUP)

# ==========================================

_players_lock = threading.Lock()

_PLAYERS_CACHE = []





def _init_players_cache():

    global _PLAYERS_CACHE

    try:

        if os.path.exists(PLAYERS_PATH):

            with open(PLAYERS_PATH, "r", encoding="utf-8") as f:

                _PLAYERS_CACHE = json.load(f)

    except Exception:

        _PLAYERS_CACHE = []





def get_all_players():

    with _players_lock:

        return list(_PLAYERS_CACHE)





def save_all_players(players_list):

    global _PLAYERS_CACHE

    with _players_lock:

        _PLAYERS_CACHE = players_list

        # Đồng bộ ra file JSON nếu ổ đĩa cho phép

        try:

            _ensure_data_dir()

            with open(PLAYERS_PATH, "w", encoding="utf-8") as f:

                json.dump(_PLAYERS_CACHE, f, ensure_ascii=False, indent=2)

        except Exception:

            pass  # Nếu ổ đĩa bị khóa/xóa, RAM vẫn giữ dữ liệu an toàn





# Nạp dữ liệu vào RAM ngay khi khởi chạy app

_init_players_cache()





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

    answer = str(data.get("answer") or "").strip()



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

    return jsonify(get_all_players())





@app.route("/api/players", methods=["POST"])

def set_players():

    if not session.get("is_tech"):

        return jsonify({"ok": False, "error": "unauthorized"}), 403



    data = request.get_json(silent=True)



    # Xử lý linh hoạt cả 2 kiểu gửi từ Frontend: [...] hoặc {"players": [...]}

    if isinstance(data, list):

        players = data

    elif isinstance(data, dict):

        players = data.get("players")

    else:

        players = None



    if not isinstance(players, list):

        return jsonify({"ok": False, "error": "invalid_payload"}), 400



    save_all_players(players)

    return jsonify({"ok": True, "count": len(players)})





@app.route("/api/admin/stats")

def admin_stats():

    if not session.get("is_tech"):

        return jsonify({"ok": False, "error": "unauthorized"}), 403

    return jsonify({

        "ok": True,

        "online_now": _count_online(),

        "total_visits": _load_total_visits(),

        "players_count": len(get_all_players()),

    })





if __name__ == "__main__":

    _ensure_data_dir()

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port) 

