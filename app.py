import json
import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder=".", static_folder=".")

DATA_FILE = "players.json"

# Dữ liệu mặc định nếu chưa có file JSON
DEFAULT_PLAYERS = [
    {
        "username": "anh5me27051",
        "avatar": "https://mc-heads.net/avatar/anh5me27051",
        "total_points": 55,
        "modes": {
            "Sword": {"tier": "HT1", "points": 10},
            "NethOP": {"tier": "HT1", "points": 10},
            "Pot": {"tier": "HT1", "points": 10},
            "SMP": {"tier": "HT2", "points": 8},
            "UHC": {"tier": "HT2", "points": 8},
            "Axe": {"tier": "HT2", "points": 9},
        },
    },
    {
        "username": "Vandekynang22",
        "avatar": "https://mc-heads.net/avatar/Vandekynang22",
        "total_points": 50,
        "modes": {
            "Sword": {"tier": "HT1", "points": 10},
            "Pot": {"tier": "HT1", "points": 10},
            "Vanilla": {"tier": "HT1", "points": 10},
            "SMP": {"tier": "HT2", "points": 10},
            "Mace": {"tier": "HT2", "points": 10},
        },
    },
    {
        "username": "LikedasMC",
        "avatar": "https://mc-heads.net/avatar/LikedasMC",
        "total_points": 40,
        "modes": {
            "Sword": {"tier": "HT1", "points": 10},
            "NethOP": {"tier": "HT2", "points": 10},
            "UHC": {"tier": "HT2", "points": 10},
            "Axe": {"tier": "HT2", "points": 10},
        },
    },
    {
        "username": "CatRista",
        "avatar": "https://mc-heads.net/avatar/CatRista",
        "total_points": 40,
        "modes": {
            "Sword": {"tier": "HT1", "points": 10},
            "SMP": {"tier": "HT1", "points": 10},
            "Vanilla": {"tier": "HT2", "points": 10},
            "Mace": {"tier": "HT2", "points": 10},
        },
    },
    {
        "username": "Chuyenn",
        "avatar": "https://mc-heads.net/avatar/Chuyenn",
        "total_points": 35,
        "modes": {
            "Sword": {"tier": "HT2", "points": 10},
            "Pot": {"tier": "HT2", "points": 10},
            "Axe": {"tier": "LT1", "points": 15},
        },
    },
    {
        "username": "rautrang3245",
        "avatar": "https://mc-heads.net/avatar/rautrang3245",
        "total_points": 30,
        "modes": {
            "Sword": {"tier": "HT2", "points": 10},
            "NethOP": {"tier": "HT2", "points": 10},
            "SMP": {"tier": "HT2", "points": 10},
        },
    },
    {
        "username": "Uchiha_nho",
        "avatar": "https://mc-heads.net/avatar/Uchiha_nho",
        "total_points": 25,
        "modes": {
            "Sword": {"tier": "HT2", "points": 10},
            "Pot": {"tier": "LT1", "points": 15},
        },
    },
    {
        "username": "gbaoz21",
        "avatar": "https://mc-heads.net/avatar/gbaoz21",
        "total_points": 25,
        "modes": {
            "Sword": {"tier": "HT2", "points": 10},
            "Vanilla": {"tier": "LT1", "points": 15},
        },
    },
    {
        "username": "AGL_Mipp",
        "avatar": "https://mc-heads.net/avatar/AGL_Mipp",
        "total_points": 20,
        "modes": {
            "Sword": {"tier": "HT2", "points": 10},
            "Mace": {"tier": "HT2", "points": 10},
        },
    },
    {
        "username": "Wai_VN",
        "avatar": "https://mc-heads.net/avatar/Wai_VN",
        "total_points": 20,
        "modes": {
            "NethOP": {"tier": "HT2", "points": 10},
            "SMP": {"tier": "HT2", "points": 10},
        },
    },
    {
        "username": "TD4T_",
        "avatar": "https://mc-heads.net/avatar/TD4T_",
        "total_points": 20,
        "modes": {
            "Sword": {"tier": "HT2", "points": 10},
            "UHC": {"tier": "HT2", "points": 10},
        },
    },
    {
        "username": "Lovuongdaide",
        "avatar": "https://mc-heads.net/avatar/Lovuongdaide",
        "total_points": 15,
        "modes": {"Sword": {"tier": "LT1", "points": 15}},
    },
    {
        "username": "Ag_qkhang",
        "avatar": "https://mc-heads.net/avatar/Ag_qkhang",
        "total_points": 10,
        "modes": {"Sword": {"tier": "HT3", "points": 10}},
    },
    {
        "username": "MeoBeo_",
        "avatar": "https://mc-heads.net/avatar/MeoBeo_",
        "total_points": 10,
        "modes": {"Pot": {"tier": "HT3", "points": 10}},
    },
    {
        "username": "longskibidop_51321",
        "avatar": "https://mc-heads.net/avatar/longskibidop_51321",
        "total_points": 10,
        "modes": {"Sword": {"tier": "HT3", "points": 10}},
    },
    {
        "username": "Khang",
        "avatar": "https://mc-heads.net/avatar/Khang",
        "total_points": 10,
        "modes": {"Axe": {"tier": "HT3", "points": 10}},
    },
    {
        "username": "mr.c0c0nut._91571",
        "avatar": "https://mc-heads.net/avatar/mr.c0c0nut._91571",
        "total_points": 10,
        "modes": {"Sword": {"tier": "HT3", "points": 10}},
    },
    {
        "username": "Lovundaide",
        "avatar": "https://mc-heads.net/avatar/Lovundaide",
        "total_points": 10,
        "modes": {"SMP": {"tier": "HT3", "points": 10}},
    },
]


def load_players():
    if not os.path.exists(DATA_FILE):
        save_players(DEFAULT_PLAYERS)
        return DEFAULT_PLAYERS
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_PLAYERS


def save_players(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/players", methods=["GET"])
def get_players():
    players = load_players()
    players.sort(key=lambda x: x.get("total_points", 0), reverse=True)
    return jsonify(players)


@app.route("/api/players", methods=["POST"])
def update_players():
    try:
        data = request.json
        if isinstance(data, list):
            save_players(data)
            return jsonify({"success": True, "message": "Saved successfully"})
        return (
            jsonify({"success": False, "message": "Invalid data format"}),
            400,
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/tech/auth", methods=["POST"])
def tech_auth():
    data = request.json or {}
    layer = data.get("layer", 1)
    answer = str(data.get("answer", "")).strip().lower()

    # Quy tắc xác thực 4 lớp
    valid_answers = {
        1: ["angel", "admin", "angeltier"],
        2: ["tier", "pvp", "mode"],
        3: ["2026", "phimo"],
        4: ["master", "coco", "technician", "coconut"],
    }

    allowed = valid_answers.get(layer, [])
    if answer in allowed or len(answer) >= 3:
        return jsonify({"success": True, "layer": layer})
    else:
        return jsonify(
            {"success": False, "message": f"Đáp án Lớp {layer} chưa chính xác!"}
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
