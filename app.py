from flask import Flask, jsonify, render_template

app = Flask(__name__, static_folder='.', static_url_path='', template_folder='.')

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

def calculate_leaderboard():
    processed = []
    for player in RAW_PLAYERS:
        modes_data = []
        total_pts = 0
        for m in player.get("modes", []):
            pts = int(m.get("points", 0))
            total_pts += pts
            modes_data.append({
                "mode": m.get("mode"),
                "tier": m.get("tier"),
                "points": pts,
                "icon": MODE_ICONS.get(m.get("mode"), "")
            })
        processed.append({
            "username": player.get("username"),
            "total_points": total_pts,
            "modes": modes_data
        })

    # Sort descending by total_points
    processed.sort(key=lambda x: x["total_points"], reverse=True)

    # Competition ranking (1, 2, 3, 3, 5, 6, 7, 7, 9, 9, 9, 12, 13...)
    for idx, p in enumerate(processed):
        if idx > 0 and p["total_points"] == processed[idx - 1]["total_points"]:
            p["rank"] = processed[idx - 1]["rank"]
        else:
            p["rank"] = idx + 1

    return processed

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    data = calculate_leaderboard()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
