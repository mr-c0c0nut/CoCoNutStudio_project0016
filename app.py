import os
from flask import Flask, render_template, jsonify

base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

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

ALL_MODES = ["Sword", "Axe", "UHC", "SMP", "NethOP", "Pot", "Mace", "Vanilla"]

# Single Source of Truth - Đúng 18 Player
RAW_PLAYERS = [
    {
        "username": "anh5me27051",
        "total_points": 55,
        "modes": {"UHC": {"tier": "HT4", "points": 25}, "Axe": {"tier": "LT4", "points": 20}, "Sword": {"tier": "LT5", "points": 10}}
    },
    {
        "username": "Vandekynang22",
        "total_points": 50,
        "modes": {"UHC": {"tier": "HT4", "points": 25}, "Axe": {"tier": "HT5", "points": 15}, "Sword": {"tier": "LT5", "points": 10}}
    },
    {
        "username": "LikedasMC",
        "total_points": 40,
        "modes": {"Sword": {"tier": "HT5", "points": 15}, "Axe": {"tier": "HT5", "points": 15}, "UHC": {"tier": "LT5", "points": 10}}
    },
    {
        "username": "CatRista",
        "total_points": 40,
        "modes": {"UHC": {"tier": "LT4", "points": 20}, "Axe": {"tier": "LT4", "points": 20}}
    },
    {
        "username": "Chuyenn",
        "total_points": 35,
        "modes": {"Sword": {"tier": "LT4", "points": 20}, "UHC": {"tier": "HT5", "points": 15}}
    },
    {
        "username": "rautrang3245",
        "total_points": 30,
        "modes": {"Sword": {"tier": "LT3", "points": 30}}
    },
    {
        "username": "Uchiha_nho",
        "total_points": 25,
        "modes": {"Sword": {"tier": "HT4", "points": 25}}
    },
    {
        "username": "gbaoz21",
        "total_points": 25,
        "modes": {"Sword": {"tier": "HT4", "points": 25}}
    },
    {
        "username": "AGL_Mipp",
        "total_points": 20,
        "modes": {"Sword": {"tier": "LT5", "points": 10}, "SMP": {"tier": "LT5", "points": 10}}
    },
    {
        "username": "Wai_VN",
        "total_points": 20,
        "modes": {"Sword": {"tier": "LT4", "points": 20}}
    },
    {
        "username": "TD4T_",
        "total_points": 20,
        "modes": {"UHC": {"tier": "LT4", "points": 20}}
    },
    {
        "username": "Lovuongdaide",
        "total_points": 15,
        "modes": {"UHC": {"tier": "HT5", "points": 15}}
    },
    {
        "username": "Ag_qkhang",
        "total_points": 10,
        "modes": {"Sword": {"tier": "LT5", "points": 10}}
    },
    {
        "username": "MeoBeo_",
        "total_points": 10,
        "modes": {"UHC": {"tier": "LT5", "points": 10}}
    },
    {
        "username": "longskibidop_51321",
        "total_points": 10,
        "modes": {"UHC": {"tier": "LT5", "points": 10}}
    },
    {
        "username": "Khang",
        "total_points": 10,
        "modes": {"Vanilla": {"tier": "LT5", "points": 10}}
    },
    {
        "username": "mr.c0c0nut._91571",
        "total_points": 10,
        "modes": {"Sword": {"tier": "LT5", "points": 10}}
    },
    {
        "username": "Lovundaide",
        "total_points": 10,
        "modes": {"UHC": {"tier": "LT5", "points": 10}}
    }
]

def build_leaderboard():
    processed = []
    
    # 1. Chuẩn hóa dữ liệu theo tất cả các Modes
    for p in RAW_PLAYERS:
        player_modes = {}
        for m in ALL_MODES:
            if m in p["modes"]:
                player_modes[m] = {
                    "tier": p["modes"][m]["tier"],
                    "points": p["modes"][m]["points"],
                    "icon": MODE_ICONS.get(m, "")
                }
            else:
                player_modes[m] = {
                    "tier": "-",
                    "points": 0,
                    "icon": MODE_ICONS.get(m, "")
                }
                
        processed.append({
            "username": p["username"],
            "total_points": p["total_points"],
            "modes": player_modes
        })
        
    # 2. Sắp xếp điểm giảm dần
    processed.sort(key=lambda x: x["total_points"], reverse=True)
    
    # 3. Competition Ranking Calculation (55=#1, 50=#2, 40=#3, 40=#3, 35=#5, ...)
    current_rank = 1
    for i in range(len(processed)):
        if i > 0 and processed[i]["total_points"] < processed[i - 1]["total_points"]:
            current_rank = i + 1
        processed[i]["rank"] = current_rank
        
    return processed

@app.route("/")
def index():
    leaderboard_data = build_leaderboard()
    return render_template(
        "index.html", 
        players=leaderboard_data,
        all_modes=ALL_MODES,
        mode_icons=MODE_ICONS
    )

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    leaderboard_data = build_leaderboard()
    return jsonify({
        "all_modes": ALL_MODES,
        "mode_icons": MODE_ICONS,
        "players": leaderboard_data
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
