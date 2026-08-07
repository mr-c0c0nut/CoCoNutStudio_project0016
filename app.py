import os
import json
from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "coco_secret_key_2026")

MODE_ICONS = {
    "Mace": "https://i.ibb.co/cXcHtW5c/1533764190723113050.webp",
    "Axe": "https://i.ibb.co/zW8WcJKh/1533764227607560233.webp",
    "Sword": "https://i.ibb.co/yFmTKyXC/1533764260486844488.webp",
    "SMP": "https://i.ibb.co/C3RjZR8v/1533764288055873638.webp",
    "NethOP": "https://i.ibb.co/G349PxWx/1533764316262826025.webp",
    "Pot": "https://i.ibb.co/ynR4j8kp/1533764426941993140.webp",
    "UHC": "https://i.ibb.co/nMSsgPcv/1533764468876771448.webp",
    "Vanilla": "https://i.ibb.co/5hPZXd0S/1533764503161012344.webp"
}

# Source of Truth - Danh sách 18 Players
PLAYERS_DATA = [
    {
        "username": "anh5me27051",
        "modes": [
            {"mode": "UHC", "tier": "HT4", "points": 25},
            {"mode": "Axe", "tier": "LT4", "points": 20},
            {"mode": "Sword", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "Vandekynang22",
        "modes": [
            {"mode": "UHC", "tier": "HT4", "points": 25},
            {"mode": "Axe", "tier": "HT5", "points": 15},
            {"mode": "Sword", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "LikedasMC",
        "modes": [
            {"mode": "Sword", "tier": "HT5", "points": 15},
            {"mode": "Axe", "tier": "HT5", "points": 15},
            {"mode": "UHC", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "CatRista",
        "modes": [
            {"mode": "UHC", "tier": "LT4", "points": 20},
            {"mode": "Axe", "tier": "LT4", "points": 20}
        ]
    },
    {
        "username": "Chuyenn",
        "modes": [
            {"mode": "Sword", "tier": "LT4", "points": 20},
            {"mode": "UHC", "tier": "HT5", "points": 15}
        ]
    },
    {
        "username": "rautrang3245",
        "modes": [
            {"mode": "Sword", "tier": "LT3", "points": 30}
        ]
    },
    {
        "username": "Uchiha_nho",
        "modes": [
            {"mode": "Sword", "tier": "HT4", "points": 25}
        ]
    },
    {
        "username": "gbaoz21",
        "modes": [
            {"mode": "Sword", "tier": "HT4", "points": 25}
        ]
    },
    {
        "username": "AGL_Mipp",
        "modes": [
            {"mode": "Sword", "tier": "LT5", "points": 10},
            {"mode": "SMP", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "Wai_VN",
        "modes": [
            {"mode": "Sword", "tier": "LT4", "points": 20}
        ]
    },
    {
        "username": "TD4T_",
        "modes": [
            {"mode": "UHC", "tier": "LT4", "points": 20}
        ]
    },
    {
        "username": "Lovuongdaide",
        "modes": [
            {"mode": "UHC", "tier": "HT5", "points": 15}
        ]
    },
    {
        "username": "Ag_qkhang",
        "modes": [
            {"mode": "Sword", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "MeoBeo_",
        "modes": [
            {"mode": "UHC", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "longskibidop_51321",
        "modes": [
            {"mode": "UHC", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "Khang",
        "modes": [
            {"mode": "Vanilla", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "mr.c0c0nut._91571",
        "modes": [
            {"mode": "Sword", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "Lovundaide",
        "modes": [
            {"mode": "UHC", "tier": "LT5", "points": 10}
        ]
    }
]

def calculate_leaderboard():
    """Xử lý tính tổng điểm, gắn icon mode và gán hạng (ranking logic)."""
    processed = []
    for item in PLAYERS_DATA:
        modes = item.get("modes", [])
        # Nếu data cũ dạng phẳng (mode, tier, points trực tiếp)
        if not modes and "mode" in item:
            modes = [{"mode": item.get("mode"), "tier": item.get("tier"), "points": item.get("points", 0)}]
            
        total_pts = sum(m.get("points", 0) for m in modes)
        
        # Gắn icon cho từng mode
        formatted_modes = []
        for m in modes:
            m_name = m.get("mode", "")
            formatted_modes.append({
                "mode": m_name,
                "tier": m.get("tier", ""),
                "points": m.get("points", 0),
                "icon": MODE_ICONS.get(m_name, "")
            })

        processed.append({
            "username": item.get("username"),
            "total_points": total_pts,
            "modes": formatted_modes,
            # Giữ các trường phẳng cho Admin Panel nếu cần
            "mode": formatted_modes[0]["mode"] if formatted_modes else "",
            "tier": formatted_modes[0]["tier"] if formatted_modes else "",
            "points": total_pts
        })

    # Sắp xếp giảm dần theo điểm
    processed.sort(key=lambda x: x["total_points"], reverse=True)

    # Tính toán Rank (55 -> #1, 50 -> #2, 40 -> #3, 40 -> #3, 35 -> #5,...)
    current_rank = 1
    for i, player in enumerate(processed):
        if i > 0 and player["total_points"] < processed[i - 1]["total_points"]:
            current_rank = i + 1
        player["rank"] = current_rank

    return processed

@app.route("/")
def index():
    leaderboard = calculate_leaderboard()
    return render_template("index.html", players=leaderboard, mode_icons=MODE_ICONS)

@app.route("/api/players", methods=["GET", "POST", "PUT", "DELETE"])
def handle_players_api():
    global PLAYERS_DATA
    if request.method == "GET":
        return jsonify(calculate_leaderboard())
    
    elif request.method == "POST":
        data = request.json or {}
        username = data.get("username")
        modes = data.get("modes", [])
        
        # Hỗ trợ Admin Panel gửi dạng đơn giản
        if not modes and "mode" in data:
            modes = [{"mode": data.get("mode"), "tier": data.get("tier"), "points": int(data.get("points", 0))}]
            
        if username:
            PLAYERS_DATA.append({"username": username, "modes": modes})
            return jsonify({"status": "success", "message": "Player added successfully"}), 201
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    elif request.method == "DELETE":
        username = request.args.get("username") or (request.json and request.json.get("username"))
        if username:
            PLAYERS_DATA = [p for p in PLAYERS_DATA if p.get("username") != username]
            return jsonify({"status": "success", "message": "Player deleted"}), 200
        return jsonify({"status": "error", "message": "Missing username"}), 400

    return jsonify({"status": "error", "message": "Method not allowed"}), 405

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
