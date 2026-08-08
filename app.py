from flask import Flask, render_template, jsonify

app = Flask(__name__)

# ---------------------------------------------------------
# 1. ICON MAPPING
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 2. PLAYER DATA
# ---------------------------------------------------------
RAW_PLAYERS = [
    {
        "username": "anh5me27051",
        "modes": [
            {"name": "UHC", "tier": "HT4", "points": 25},
            {"name": "Axe", "tier": "LT4", "points": 20},
            {"name": "Sword", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "Vandekynang22",
        "modes": [
            {"name": "UHC", "tier": "HT4", "points": 25},
            {"name": "Axe", "tier": "HT5", "points": 15},
            {"name": "Sword", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "LikedasMC",
        "modes": [
            {"name": "Sword", "tier": "HT5", "points": 15},
            {"name": "Axe", "tier": "HT5", "points": 15},
            {"name": "UHC", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "CatRista",
        "modes": [
            {"name": "UHC", "tier": "LT4", "points": 20},
            {"name": "Axe", "tier": "LT4", "points": 20}
        ]
    },
    {
        "username": "Chuyenn",
        "modes": [
            {"name": "Sword", "tier": "LT4", "points": 20},
            {"name": "UHC", "tier": "HT5", "points": 15}
        ]
    },
    {
        "username": "rautrang3245",
        "modes": [
            {"name": "Sword", "tier": "LT3", "points": 30}
        ]
    },
    {
        "username": "Uchiha_nho",
        "modes": [
            {"name": "Sword", "tier": "HT4", "points": 25}
        ]
    },
    {
        "username": "gbaoz21",
        "modes": [
            {"name": "Sword", "tier": "HT4", "points": 25}
        ]
    },
    {
        "username": "AGL_Mipp",
        "modes": [
            {"name": "Sword", "tier": "LT5", "points": 10},
            {"name": "SMP", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "Wai_VN",
        "modes": [
            {"name": "Sword", "tier": "LT4", "points": 20}
        ]
    },
    {
        "username": "TD4T_",
        "modes": [
            {"name": "UHC", "tier": "LT4", "points": 20}
        ]
    },
    {
        "username": "Lovuongdaide",
        "modes": [
            {"name": "UHC", "tier": "HT5", "points": 15}
        ]
    },
    {
        "username": "Ag_qkhang",
        "modes": [
            {"name": "Sword", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "MeoBeo_",
        "modes": [
            {"name": "UHC", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "longskibidop_51321",
        "modes": [
            {"name": "UHC", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "Khang",
        "modes": [
            {"name": "Vanilla", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "mr.c0c0nut._91571",
        "modes": [
            {"name": "Sword", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "Lovundaide",
        "modes": [
            {"name": "UHC", "tier": "LT5", "points": 10}
        ]
    }
]

# ---------------------------------------------------------
# 3. HELPER PROCESSOR
# ---------------------------------------------------------
def calculate_leaderboard():
    processed = []

    for player in RAW_PLAYERS:
        total_points = sum(m["points"] for m in player["modes"])
        
        formatted_modes = []
        for m in player["modes"]:
            formatted_modes.append({
                "name": m["name"],
                "tier": m["tier"],
                "points": m["points"],
                "icon": MODE_ICONS.get(m["name"], "")
            })

        processed.append({
            "username": player["username"],
            "total_points": total_points,
            "modes": formatted_modes
        })

    # Sắp xếp giảm dần theo điểm
    processed.sort(key=lambda x: x["total_points"], reverse=True)

    # Tính Competition Rank (#1, #2, #3, #3, #5, #6, #7, #7, #9,...)
    current_rank = 1
    for i in range(len(processed)):
        if i > 0 and processed[i]["total_points"] < processed[i - 1]["total_points"]:
            current_rank = i + 1
        processed[i]["rank"] = current_rank

    return processed

# ---------------------------------------------------------
# 4. ROUTES & API ENDPOINTS
# ---------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/leaderboard", methods=["GET"])
@app.route("/api/players", methods=["GET"])
@app.route("/api/rankings", methods=["GET"])
def get_leaderboard():
    data = calculate_leaderboard()
    return jsonify({
        "status": "success",
        "players": data,
        "data": data
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
