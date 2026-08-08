import os
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates', static_folder='static')

# ---------------------------------------------------------
# 1. MODE ICONS MAPPING (SOURCE OF TRUTH)
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
# 2. RAW PLAYER DATA
# ---------------------------------------------------------
RAW_PLAYERS = [
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

# ---------------------------------------------------------
# 3. HELPER PROCESSOR (COMPETITION RANKING)
# ---------------------------------------------------------
def get_processed_leaderboard():
    processed = []
    
    for p in RAW_PLAYERS:
        total_pts = sum(m["points"] for m in p["modes"])
        
        modes_with_icons = []
        for m in p["modes"]:
            modes_with_icons.append({
                "mode": m["mode"],
                "tier": m["tier"],
                "points": m["points"],
                "icon": MODE_ICONS.get(m["mode"], "")
            })
            
        processed.append({
            "username": p["username"],
            "total_points": total_pts,
            "modes": modes_with_icons
        })

    # Sort descending by total points, then alphabetically by username
    processed.sort(key=lambda x: (-x["total_points"], x["username"].lower()))

    # Calculate Competition Ranking (1, 2, 3, 3, 5...)
    current_rank = 1
    for i, player in enumerate(processed):
        if i > 0 and player["total_points"] == processed[i - 1]["total_points"]:
            player["rank"] = processed[i - 1]["rank"]
        else:
            player["rank"] = i + 1

    return processed

# ---------------------------------------------------------
# 4. ROUTES
# ---------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/leaderboard")
def api_leaderboard():
    data = get_processed_leaderboard()
    return jsonify({
        "status": "success",
        "total_players": len(data),
        "data": data,
        "mode_icons": MODE_ICONS
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
